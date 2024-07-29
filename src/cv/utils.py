import asyncio
import base64
from typing import Dict, List, Optional, Tuple

import httpx

from src.config import settings
from src.cv.exceptions import InternalServerError, GitHubFailedToFetchException

github_api_url = 'https://api.github.com'
headers = httpx.Headers({'Authorization': f'Bearer {settings.app.github_pat_token}'})


def remove_none_values(data: Dict) -> Dict:
    return {k: v for k, v in data.items() if v not in [None, '', [], {}]}


async def fetch_repo_languages(client: httpx.AsyncClient, languages_url: str) -> Optional[Dict]:
    try:
        response = await client.get(languages_url)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError:
        return None


async def fetch_repo_readme(client: httpx.AsyncClient, full_name: str) -> Optional[str]:
    try:
        response = await client.get(f'{github_api_url}/repos/{full_name}/readme')
        response.raise_for_status()
        response_data = response.json()
        if response_data.get('encoding') == 'base64':
            return base64.b64decode(response_data.get('content')).decode('utf-8')
        return None
    except httpx.HTTPStatusError:
        return None


async def fetch_user_and_repos(client: httpx.AsyncClient, username: str) -> Tuple[Dict, List[Dict]]:
    user_url, repos_url = f'{github_api_url}/users/{username}', f'{github_api_url}/users/{username}/repos'
    user_task, repos_task = client.get(user_url), client.get(repos_url)

    try:
        user_response, repos_response = await asyncio.gather(user_task, repos_task)
        user_response.raise_for_status()
        repos_response.raise_for_status()
        user_data, repos_data = user_response.json(), repos_response.json()

        filtered_user_data = remove_none_values(
            {
                'login': user_data.get('login'),
                'avatar_url': user_data.get('avatar_url'),
                'html_url': user_data.get('html_url'),
                'repos_url': user_data.get('repos_url'),
                'name': user_data.get('name'),
                'company': user_data.get('company'),
                'blog': user_data.get('blog'),
                'location': user_data.get('location'),
                'email': user_data.get('email'),
                'bio': user_data.get('bio'),
                'created_at': user_data.get('created_at'),
                'updated_at': user_data.get('updated_at'),
            },
        )

        filtered_repos_data = [
            remove_none_values(
                {
                    'name': repo.get('name'),
                    'full_name': repo.get('full_name'),
                    'html_url': repo.get('html_url'),
                    'description': repo.get('description'),
                    'languages_url': repo.get('languages_url'),
                    'created_at': repo.get('created_at'),
                    'updated_at': repo.get('updated_at'),
                    'pushed_at': repo.get('pushed_at'),
                    'language': repo.get('language'),
                    'topics': repo.get('topics'),
                },
            ) for repo in repos_data
        ]

        return filtered_user_data, filtered_repos_data
    except httpx.HTTPStatusError:
        raise GitHubFailedToFetchException
    except Exception:
        raise InternalServerError


async def fetch_and_update_repo_details(client: httpx.AsyncClient, repos_data: List[Dict]) -> List[Dict]:
    languages_tasks = [fetch_repo_languages(client, repo.get('languages_url')) for repo in repos_data]
    readme_tasks = [fetch_repo_readme(client, repo.get('full_name')) for repo in repos_data]

    languages_results, readme_results = await asyncio.gather(
        asyncio.gather(*languages_tasks),
        asyncio.gather(*readme_tasks),
    )

    for repo, languages, readme in zip(repos_data, languages_results, readme_results):
        repo['languages'] = languages if languages else None

        if repo.get('description') and readme:
            repo['description'] = f'{repo.get("description")}\n\n{readme}'
        if not repo.get('description') and readme:
            repo['description'] = readme

    return repos_data


async def collect_all_data_from_github(username: str) -> Dict:
    async with httpx.AsyncClient(headers=headers) as client:
        user_data, repos_data = await fetch_user_and_repos(client, username)
        repos_data = await fetch_and_update_repo_details(client, repos_data)
        user_data['repos'] = repos_data
        return user_data
