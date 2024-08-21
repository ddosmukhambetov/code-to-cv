from fastapi import HTTPException, status

GitHubFailedToFetchException = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail='Failed to fetch data from GitHub',
)

InvalidProfileLinkException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Invalid profile link',
)

CvDataGenerationException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Failed to generate CV data',
)

PdfGenerationException = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Failed to generate PDF file',
)
