from typing import Dict

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from src.config import settings
from src.cv.exceptions import InternalServerError


def generate_html_from_json(cv_data: Dict) -> str:
    env = Environment(loader=FileSystemLoader('templates/cv'))
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
