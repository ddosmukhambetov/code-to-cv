import json
from typing import Dict

import openai
from jinja2 import Environment, FileSystemLoader
from openai import AsyncOpenAI
from weasyprint import HTML

from app.core.config import settings
from app.core.database import redis_manager
from app.cvs.exceptions import PdfGenerationException, CvDataGenerationException
from app.cvs.schemas import CvGenerateSchema
from app.cvs.utils.fetch_data_from_github import collect_user_and_repos_data_from_github


async def generate_cv_data(username: str) -> dict:
    cache_key = f'github_user_data:{username}'
    if cached_data := await redis_manager.get(cache_key):
        github_user_data = cached_data
    else:
        github_user_data = await collect_user_and_repos_data_from_github(username)
        await redis_manager.set(cache_key, github_user_data, expire=300)

    prompt = """
    You are an expert AI assistant with the capability to generate professional resumes.
    Your task is to create a resume that is well-organized, polished, and written from the first-person perspective.
    The resume should present the individual's skills, experience, and achievements in a confident and professional
    tone. If any necessary details are missing from the provided information, generate content that fits naturally and
    enhances the overall presentation. Ensure that the resume is suitable for applying to various technical positions
    and reflects a high standard of quality.
    """

    CvGenerateSchema.PersonalInformation.name = github_user_data.get('name', 'login')
    CvGenerateSchema.PersonalInformation.github_profile_link = github_user_data.get('html_url', '')

    client = AsyncOpenAI(api_key=settings.api_keys.openai_key)
    try:
        completion = await client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": json.dumps(github_user_data)},
            ],
            temperature=0.7,
            max_tokens=1500,
            tools=[openai.pydantic_function_tool(CvGenerateSchema)],
        )
    except Exception:
        raise CvDataGenerationException
    response_content = completion.choices[0].message.tool_calls[0].function.arguments
    return json.loads(response_content)


def generate_cv_html_from_json(cv_data: Dict, template_name: str) -> str:
    template_dir = settings.media.cv_templates_path / template_name
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('template.html')
    return template.render(cv_data=cv_data)


def generate_cv_pdf_from_html(cv_data: Dict, template_name: str) -> str:
    html_content = generate_cv_html_from_json(template_name=template_name, cv_data=cv_data)
    template_dir = settings.media.cv_templates_path / template_name
    output_path = settings.media.get_cv_pdf_file_path
    try:
        HTML(string=html_content, base_url=template_dir).write_pdf(output_path)
        return output_path
    except Exception:
        raise PdfGenerationException
