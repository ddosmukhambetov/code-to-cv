from fastapi import HTTPException, status

QuestionAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='409_QUESTION_ALREADY_EXISTS',
)

QuestionNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='404_QUESTION_NOT_FOUND',
)
