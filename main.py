# api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.bus_controller import bus_router
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
import uvicorn


app = FastAPI()

# https
app.add_middleware(HTTPSRedirectMiddleware)

# CORS 설정
origins = ["*"]  # 필요한 출처를 지정해야 하며, *는 모든 출처를 허용함을 의미합니다.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)# CORS 설정

app.include_router(bus_router, prefix="/metabusapi")


if __name__ == "__main__":
    # HTTP 서버 실행 (포트 8000) 사용자용
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
     # HTTPS 서버 실행 (포트 8443) 개발자용
    uvicorn.run("main:app",host="0.0.0.0",port=8443,reload=True, ssl_keyfile="ssl키경로", ssl_certfile="ssl키경로")



