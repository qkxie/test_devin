from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Data Analysis API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Data Analysis API is running"}

@app.post("/api/analyze")
async def analyze_file(file: UploadFile = File(...)):
    """
    接收文件上传并返回确认信息
    """
    return JSONResponse(
        content={
            "filename": file.filename,
            "status": "received"
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
