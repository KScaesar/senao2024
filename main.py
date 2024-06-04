import uvicorn

import src.adapters.api.FastAPI as FastAPI


# fastapi dev main.py --port 12450
api = FastAPI.router()


if __name__ == "__main__":
    # python main.py
    router = FastAPI.router()
    uvicorn.run(router, port=12450)
