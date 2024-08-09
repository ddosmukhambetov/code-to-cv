import json
from typing import Dict

from jinja2 import Environment, FileSystemLoader
from openai import AsyncOpenAI
from weasyprint import HTML

from src.config import settings
from src.cvs.exceptions import InternalServerError, InvalidProfileLinkException
from src.cvs.utils.github_api import collect_all_data_from_github
from templates.cvs.prompt import cv_system_prompt


async def generate_cv_text(profile_link: str) -> dict:
    if profile_link.startswith('https://github.com/'):
        username = profile_link.split('/')[-1]
    else:
        raise InvalidProfileLinkException
    github_user_data = await collect_all_data_from_github(username)

    system_prompt = cv_system_prompt.format(
        name=github_user_data.get('name', 'login'),
        html_url=github_user_data.get('html_url'),
        bio=github_user_data.get('bio'),
        location=github_user_data.get('location')
    )

    client = AsyncOpenAI(api_key=settings.app.openai_api_key)
    completion = await client.chat.completions.create(
        model="gpt-4o",
        response_format={'type': 'json_object'},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(github_user_data)},
        ],
        temperature=0.7,
    )
    response_content = completion.choices[0].message.content
    return json.loads(response_content)


def generate_html_from_json(cv_data: Dict) -> str:
    env = Environment(loader=FileSystemLoader('templates/cvs'))
    template = env.get_template('pdf.html')
    return template.render(cv_data=cv_data)


def generate_pdf_file(cv_data: Dict) -> tuple[str, str]:
    html_content = generate_html_from_json(cv_data)
    output_path = settings.media.get_cv_file_path()
    try:
        HTML(string=html_content).write_pdf(output_path)
        return str(output_path.name), str(output_path)
    except Exception:
        raise InternalServerError
