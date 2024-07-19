from typing import Dict, Any

from pydantic import BaseModel


def model_dump(model: BaseModel, *args, **kwargs) -> Dict[str, Any]:
    return model.model_dump(*args, **kwargs)


class CreateUpdateDict(BaseModel):
    def create_update_dict(self):
        return model_dump(
            self,
            exclude_unset=True,
            exclude={
                'id',
                'is_active',
                'created_at',
                'updated_at',
            },
        )

    def create_update_dict_superuser(self):
        return model_dump(self, exclude_unset=True, exclude={"id"})
