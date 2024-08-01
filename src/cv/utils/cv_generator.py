from typing import Dict

from weasyprint import HTML

from src.config import settings
from src.cv.exceptions import InternalServerError


def format_key(key: str) -> str:
    key = key.replace('_', ' ')
    return key.title()


def generate_html_from_json(cv_data: Dict) -> str:
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; }
            h1, h2, h3 { color: #333; }
            .section { margin-bottom: 20px; }
            .skills, .projects { list-style-type: none; padding-left: 0; }
            .skills li, .projects li { margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <h1>Resume</h1>
    """

    for key, value in cv_data.items():
        section_title = format_key(key)
        html_content += f"<div class='section'><h2>{section_title}</h2>"
        if isinstance(value, str):
            html_content += f"<p>{value}</p>"
        elif isinstance(value, list):
            html_content += "<ul>"
            for item in value:
                if isinstance(item, dict):
                    html_content += "<li><ul>"
                    for sub_key, sub_value in item.items():
                        sub_section_title = format_key(sub_key)
                        if isinstance(sub_value, list):
                            sub_value = ", ".join(sub_value)
                        html_content += f"<li><strong>{sub_section_title}:</strong> {sub_value}</li>"
                    html_content += "</ul></li>"
                else:
                    html_content += f"<li>{item}</li>"
            html_content += "</ul>"
        elif isinstance(value, dict):
            html_content += "<ul>"
            for sub_key, sub_value in value.items():
                sub_section_title = format_key(sub_key)
                if isinstance(sub_value, list):
                    sub_value = ", ".join(sub_value)
                html_content += f"<li><strong>{sub_section_title}:</strong> {sub_value}</li>"
            html_content += "</ul>"
        html_content += "</div>"
    html_content += "</body></html>"
    return html_content


def generate_pdf_file(cv_data: Dict) -> str:
    html_content = generate_html_from_json(cv_data)
    output_path = str(settings.media.get_cv_file_path())
    try:
        HTML(string=html_content).write_pdf(output_path)
        return output_path
    except Exception:
        raise InternalServerError
