# api.py
# from fastapi import APIRouter, Path, Query, HTTPException, status
from fastapi import APIRouter, HTTPException, status
# from database.connection import Database
from pymongo import MongoClient
from model.bus_service import Service
from urllib.parse import unquote


bus_router = APIRouter()

service_instance = Service()

@bus_router.get("/")
async def welcome():
    return {
            "message" : "Hello! Our Metabus OpenAPI Service ."
            , "code" : "200"
            }


@bus_router.get("/get_departure_list")
async def departure_list():

    try:
        return service_instance.get_departure_list()
    except Exception as e:
        # 기타 예외 처리
        return {
            "message" : "query does not exist! - departure-query"
            , "code" : "888"
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 요청 경로입니다",
    )

@bus_router.get("/get_destination_list")
async def destination_list(
     departure : str
    ):
    try:
        decoded_departure = unquote(departure)
        sortedDate = sorted(service_instance.get_destination_for_departure_list(decoded_departure))
        return sortedDate
    except Exception as e:
        # 기타 예외 처리
        return {
            "message" : "query does not exist! - departure-query"
            , "code" : "888"
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 요청 경로입니다",
    )

@bus_router.get("/get_bus_list")
async def bus_list(
     departure : str,
     destination : str
    ):
    try:
        decoded_departure = unquote(departure)
        decoded_destination = unquote(destination)
        datasForCheck = service_instance.get_bus_list(decoded_departure,decoded_destination)
        for item in datasForCheck:
            if item["cost"] == "":
                item["cost"] = 1500
        return datasForCheck
    except Exception as e:
        # 기타 예외 처리
        return {
            "message" : "query does not exist! - departure-query, destination-query"
            , "code" : "888"
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="존재하지 않는 요청 경로입니다",
    )
    
# @bus_router.get("/test/{todo}")
# # Optional로 값이 없으면 None을 default로 설정
# async def test(
#     todo: int = Path(..., title="아이디를 찾는 경로")
#     , name : Optional[str] = Query(None, alias="id-query")
#     ):
#     # None이면 false이기에 if 탐

#     #db
#     # buses = await bus_database.find()

#     if(name) : 
#         return {
#             "message" : name
#         }
#     # 전부 안 탔을 경우 마지막으로 타는 return
#     if 1 == todo:
#         return {
#                 "message" : "기본"
#                 }
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="존재하지 않는 요청 경로입니다",
#     )

