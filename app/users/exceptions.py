from fastapi import HTTPException, status

PermissionDeniedException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Permission denied',
)

UnauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Unauthorized',
)
