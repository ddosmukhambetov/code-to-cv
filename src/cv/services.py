import json

from openai import AsyncOpenAI

from src.config import settings
from src.cv.exceptions import InvalidProfileLinkException
from src.cv.repositories import CvRepository
from src.cv.utils.cv_generator import generate_pdf_file
from src.cv.utils.github_api import collect_all_data_from_github


class CvService:
    def __init__(self, cv_repository: CvRepository):
        self.cv_repository: CvRepository = cv_repository

    @staticmethod
    async def generate_cv_text(profile_link: str) -> dict:
        if profile_link.startswith('https://github.com/'):
            username = profile_link.split('/')[-1]
        else:
            raise InvalidProfileLinkException
        github_user_data = await collect_all_data_from_github(username)

        system_prompt = f"""
        You are a CV (Resume) generator designed to output JSON.
        You will create a professional CV for the following user based on their GitHub profile and repositories.
        The resume should be written in the first person, as if the user is writing it themselves.
        Ensure the content is concise and fits within one page.
        Make sure to include the following sections:
        1. Personal Information
        2. About Me (If provided, else generate a detailed description of the user's professional background, interests, and goals. The description should be at least 5-6 sentences long.)
        3. Skills (If provided, else generate them)
        4. Projects (If no description provided, generate a short description, add used tools and technologies)
        5. Projects Summary (If provided, else generate a summary of projects. The summary should be at least 5-6 sentences long and cover the key aspects and achievements in the user's projects.)
        6. Experience (If provided, else generate a detailed description of experience. The description should be at least 5-6 sentences long and cover key roles, responsibilities, and achievements.)
        7. Disclaimer (State that the resume was generated using AI technology)
        
        ## Personal Information
        - **Name:** {github_user_data.get('name', 'login')}
        - **Link to GitHub profile:** {github_user_data.get('html_url')})
        - **Bio:** {github_user_data.get('bio')} (If provided, else generate them)
        - **Location:** {github_user_data.get('location')} (If provided, else skip)
        - **Speaking languages:** (If provided, else generate them)
        - **Contact Information** (Contact information includes email or social media links. If provided, else skip)
        """

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

    async def generate_cv_pdf(self, profile_link: str, user_id: int):
        cv_data = await self.generate_cv_text(profile_link=profile_link)
        file_name, output_path = generate_pdf_file(cv_data=cv_data)
        return await self.cv_repository.create_one(
            profile_link=profile_link,
            file_name=file_name,
            file_path=output_path,
            cv_data=cv_data,
            user_id=user_id,
        )
