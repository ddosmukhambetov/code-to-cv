from typing import Dict

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from src.config import settings
from src.cv.exceptions import InternalServerError


def format_key(key: str) -> str:
    key = key.replace('_', ' ')
    return key.title()


def generate_html_from_json(cv_data: Dict) -> str:
    env = Environment(loader=FileSystemLoader('templates/cv'))
    template = env.get_template('main.html')
    return template.render(cv_data=cv_data)


def generate_pdf_file(cv_data: Dict) -> str:
    html_content = generate_html_from_json(cv_data)
    output_path = str(settings.media.get_cv_file_path())
    try:
        HTML(string=html_content).write_pdf(output_path)
        return output_path
    except Exception:
        raise InternalServerError
