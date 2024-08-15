from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, object_title: str = 'Object'):
        detail = f"{object_title} not found!"
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AlreadyExistsException(HTTPException):
    def __init__(self, object_title: str = 'Object'):
        detail = f"{object_title} already exists!"
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
