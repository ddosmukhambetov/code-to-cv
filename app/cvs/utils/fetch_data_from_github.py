import asyncio
import base64
from typing import Dict, List, Optional, Tuple, Any

import httpx

from app.core.config import settings
from app.cvs.exceptions import GitHubFailedToFetchException

github_api_url = 'https://api.github.com'
headers = httpx.Headers({'Authorization': f'Bearer {settings.api_keys.github_pat}'})


def remove_none_values(data: Dict) -> dict[Any, dict] | list[dict] | dict:
    if isinstance(data, dict):
        return {k: remove_none_values(v) for k, v in data.items() if v not in [None, '', [], {}]}
    elif isinstance(data, list):
        return [remove_none_values(item) for item in data if item not in [None, '', [], {}]]
    else:
        return data


async def fetch_user_and_repos_data_from_github(client: httpx.AsyncClient, username: str) -> Tuple[Dict, List[Dict]]:
    user_url = f'{github_api_url}/users/{username}'
    user_repos_url = f'{github_api_url}/users/{username}/repos?per_page=15&sort=updated'
    user_task, repos_task = client.get(user_url), client.get(user_repos_url)

    try:
        user_response, repos_response = await asyncio.gather(user_task, repos_task)
        user_response.raise_for_status()
        repos_response.raise_for_status()
        user_data, repos_data = user_response.json(), repos_response.json()

        filtered_user_data = {
            'login': user_data.get('login'),
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
        }

        filtered_repos_data = [
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
            }
            for repo in repos_data
        ]
    except Exception:
        raise GitHubFailedToFetchException

    return filtered_user_data, filtered_repos_data


async def fetch_used_languages_from_repo(client: httpx.AsyncClient, languages_url: str) -> Optional[Dict]:
    try:
        response = await client.get(languages_url)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


async def fetch_readme_description_from_repo(client: httpx.AsyncClient, full_name: str) -> Optional[str]:
    try:
        response = await client.get(f'{github_api_url}/repos/{full_name}/readme')
        response.raise_for_status()
        response_data = response.json()
        if response_data.get('encoding') == 'base64':
            return base64.b64decode(response_data.get('content')).decode('utf-8')
        return None
    except Exception:
        return None


async def add_languages_and_readme_to_repos(client: httpx.AsyncClient, repos_data: List[Dict]) -> List[Dict]:
    languages_tasks = [fetch_used_languages_from_repo(client, repo['languages_url']) for repo in repos_data]
    readme_tasks = [fetch_readme_description_from_repo(client, repo['full_name']) for repo in repos_data]

    languages_results, readme_results = await asyncio.gather(
        asyncio.gather(*languages_tasks),
        asyncio.gather(*readme_tasks),
    )

    for repo, languages, readme in zip(repos_data, languages_results, readme_results):
        repo['languages'] = languages if languages else None

        if repo.get('description') and readme:
            repo['description'] = f'{repo['description']}\n\n{readme}'
        if not repo.get('description') and readme:
            repo['description'] = readme

    return repos_data


async def collect_user_and_repos_data_from_github(username: str) -> Dict:
    async with httpx.AsyncClient(headers=headers) as client:
        user_data, repos_data = await fetch_user_and_repos_data_from_github(client, username)
        repos_data = await add_languages_and_readme_to_repos(client, repos_data)
        user_data['repos'] = repos_data
        return remove_none_values(user_data)
