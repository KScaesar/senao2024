import src.adapters.api.FastAPI as FastAPI
import uvicorn

# fastapi dev main.py --port 12450
api = FastAPI.router()

if __name__ == "__main__":
    # python main.py
    router = FastAPI.router()
    uvicorn.run(router, host="0.0.0.0", port=12450)
