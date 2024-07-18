from fastapi import HTTPException, status

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='401_TOKEN_EXPIRED',
)

TokenInvalidException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='401_TOKEN_INVALID',
)

NotAuthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='401_UNAUTHORIZED',
)

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='409_USER_ALREADY_EXISTS',
)

IncorrectCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='401_INCORRECT_CREDENTIALS',
)

PermissionDenied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='403_PERMISSION_DENIED',
)

UserNotPresentException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='404_USER_NOT_PRESENT',
)

InvalidUsernameException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='400_INVALID_USERNAME: USERNAME 4 TO 124 CHARACTERS, LETTERS, NUMBERS, DOT, UNDERSCORE, HYPHEN',
)

InvalidPasswordException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='400_INVALID_PASSWORD: MIN 8 CHARACTERS, MIN 1 LETTER, MIN 1 NUMBER, MIN 1 SYMBOL',
)
