from fastapi import HTTPException, status

CategoryAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='409_CATEGORY_ALREADY_EXISTS',
)

CategoryNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='404_CATEGORY_NOT_FOUND',
)

ParentCategoryNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='404_PARENT_CATEGORY_NOT_FOUND',
)

CategoryHasChildrenException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail='422_CATEGORY_HAS_CHILDREN',
)

ParentCategoryRecursiveException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail='422_PARENT_CATEGORY_CAN_NOT_BE_ITSELF',
)
