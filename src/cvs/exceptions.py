from fastapi import HTTPException, status

InvalidProfileLinkException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='400_INVALID_PROFILE_LINK',
)

GithubUserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='404_GITHUB_USER_NOT_FOUND',
)

GitHubUserRepositoriesNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='404_GITHUB_USER_REPOSITORIES_NOT_FOUND',
)

GitHubFailedToFetchException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='500_GITHUB_FAILED_TO_FETCH',
)

InternalServerError = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='500_INTERNAL_SERVER_ERROR',
)

CvNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='404_CV_NOT_FOUND',
)
