from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from recommender import recommend_books

app = FastAPI(
    title="Book Recommendation API",
    description="검색어 기반 도서 추천 API",
    version="1.0.0"
)


class RecommendRequest(BaseModel):
    query: str


class RecommendResponse(BaseModel):
    query: str
    recommendations: List[str]


@app.get("/")
def root():
    """
    서버 상태 확인용 엔드포인트
    """
    return {"message": "Book Recommendation API is running"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(request: RecommendRequest):
    """
    사용자 입력을 받아 도서 추천 결과를 반환
    """
    query = request.query.strip()

    if not query:
        raise HTTPException(status_code=400, detail="검색어가 비어 있습니다.")

    try:
        results = recommend_books(query)
        return RecommendResponse(
            query=query,
            recommendations=results
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"추천 처리 중 오류가 발생했습니다: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)