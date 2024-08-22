import os
from typing import Optional

from app.core.config import settings
from app.exceptions import NotFoundException


async def validate_cv_template_name(template_name: Optional[str] = 'default_cv_template') -> str:
    template_path = settings.media.cv_templates_path / template_name
    if (
            not os.path.isdir(template_path) or
            not os.path.isfile(template_path / 'template.html') or
            not os.path.isfile(template_path / 'style.css')
    ):
        raise NotFoundException('Template or CSS')
    return template_name
