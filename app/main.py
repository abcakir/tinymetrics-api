from fastapi import FastAPI

app = FastAPI(title="TinyMetrics API")

@app.get("/")
def read_root():
    return {"status": "active", "service": "TinyMetrics API"}