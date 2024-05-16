from fastapi import FastAPI, responses
from routers.todos import router as TodoRouter
from starlette import status


app = FastAPI()

app.include_router(router=TodoRouter)

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)}
    )