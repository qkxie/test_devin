from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from bug_script import analyze_user_profiles

app = FastAPI(title="Data Analysis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Data Analysis API is running"}

@app.post("/api/analyze")
async def analyze_file(file: UploadFile = File(...)):
    """
    接收CSV文件上传并返回分析结果
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="只支持CSV文件格式")
        
        content = await file.read()
        
        analysis_results = analyze_user_profiles(content)
        
        total_users = len(analysis_results)
        eligible_users = len([user for user in analysis_results if user['EligibleStatus'] == 'YES'])
        avg_score_overall = sum(user['avg_score'] for user in analysis_results) / total_users if total_users > 0 else 0
        
        location_stats = {}
        for user in analysis_results:
            location = user['Location']
            if location not in location_stats:
                location_stats[location] = {'count': 0, 'avg_score': 0, 'eligible': 0}
            location_stats[location]['count'] += 1
            location_stats[location]['avg_score'] += user['avg_score']
            if user['EligibleStatus'] == 'YES':
                location_stats[location]['eligible'] += 1
        
        for location in location_stats:
            if location_stats[location]['count'] > 0:
                location_stats[location]['avg_score'] /= location_stats[location]['count']
        
        return JSONResponse(
            content={
                "filename": file.filename,
                "status": "success",
                "summary": {
                    "total_users": total_users,
                    "eligible_users": eligible_users,
                    "eligibility_rate": round(eligible_users / total_users * 100, 1) if total_users > 0 else 0,
                    "overall_avg_score": round(avg_score_overall, 1)
                },
                "location_stats": {
                    location: {
                        "count": stats["count"],
                        "avg_score": round(stats["avg_score"], 1),
                        "eligible": stats["eligible"]
                    }
                    for location, stats in location_stats.items()
                },
                "detailed_results": analysis_results
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理错误: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
