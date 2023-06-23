# 크롤링 데이터 를 위한 API 서버
- FastAPI APIserver for Web Crowling Data 

시외버스 시간표, 노선 정보 등 OPEN API 데이터의 수집에 어려움을 겪어, 데이터 크롤링으로 자체 API 서버 구축을 하기로 결정

## 1. 스웨거 문서

https://metabus.site:8443/docs

![image](https://github.com/bong44/FastAPI_OpenAPIserver_forWebCrowlingData/assets/65393001/d8d02a81-e2e0-4261-ab26-ebd16b6631a7)


## 1.1 파이썬 어플리케이션 가상환경 준비

- virtualenv를 사용함으로 특정 패키지에 전역으로 설치하지 않아도 서로 다른 어플리케이션을 동시에 개발한 환경을 구축 가능하다.

```bash
# virtualenv 설치
$ sudo apt install python3.8-venv -y

# 현재경로에 가상환경 생성
$ python3 -m venv venv
```

- 가상환경 활성화 방법

```bash
# 가상환경 활성화
$ source venv/bin/activate

# 가상환경 비활성화
$ deactivate
```

## 1.2 패키지 설치

- 가상환경에서 필요한 패키지 설치

```bash
# 패키지 이름과 버전 명시할 txt 파일 생성
$ touch requirements.txt

# requirements.txt에 있는 내용들로 패키지 자동설치
$ pip install -r requirements.txt

# 현재 설치되어 있는 패키지들과 버전을 requirements.txt에 넣을 수도 있다
$ pip freeze > requirements.txt
```

- requirements.txt

```
anyio==3.6.2
click==8.1.3
dnspython==2.3.0
fastapi==0.95.2
h11==0.14.0
idna==3.4
sniffio==1.3.0
starlette==0.27.0
typing_extensions==4.5.0
uvicorn==0.22.0
beanie==1.11.0
```

# 2. 데이터 베이스 구축

## 2.1 MongoDB 배포 준비

- MongoDB 이미지 배포를 위한 docker-compose.yml 파일 작성

```yaml
version: "3"

services:
  
  database:
    image: mongo:5.0.15
    container_name: mymongo
    ports:
      - "몽고포트:몽고포트"
    restart: always
    volumes:
      - ./mongodbvol:/data/db

volumes:
  data:
```

- MongoDB 이미지 배포를 위한 docker-compose.yml 파일 작성

```bash
# 배포된 DB에 bash로 접속 가능
docker exec -it [컨테이너_이름 또는 컨테이너_ID] bash
```

## 2.2 MongoDB 초기 설정

- MongoDB 초기 사용자 등록

```bash
# admin 데이터베이스 접속
> use admin
#logs: switched to db admin

# 유저 생성
> db.createUser({user:"metabus",pwd:"metabus",roles: [role:"readWrite", db:"metaDb"]})

# 등록된 유저 확인 가능
> db.system.users.find()
#Logs { "_id" : "admin.metabus", "userId" : UUID("735a5e9f-75df-4329-8c9c-e1904f0e6660"), "user" : "metabus", "db" : "admin", "credentials" : { "SCRAM-SHA-1" : { "iterationCount" : 10000, "salt" : "LoBR7Cm7zDg6Ir3FvkVSXQ==", "storedKey" : "8ntBdkh4WpPlWLJyQoB8Q40vjVw=", "serverKey" : "oip6swOBYRvrYrcjfMj5Oit1v1s=" }, "SCRAM-SHA-256" : { "iterationCount" : 15000, "salt" : "2x9tPNngKh+W8E2fgx21JbdCBEHo32G/c7h2vA==", "storedKey" : "bD64Pws2REjKFHuYS/PDNhbT2eVF7vmX44qj0VIXEfs=", "serverKey" : "c+TGN88zrJb6Oyyp4IrTUH68BJ+B52Jx6kkjXbcZ/wQ=" } }, "roles" : [ { "role" : "readWrite", "db" : "myDatabase" } ] }

$ sudo docker exec -it [컨테이너명 또는 컨테이너_ID] mongo -u metabus -p metabus --authenticationDatabase admin 
# 컨테이너의 shell접속과 mongodb의 shell 접속을 동시에 실행
```

- MongoDB 데이터베이스 및 컬렉션 생성

```bash
# 데이터베이스 생성
> use myDatabase

# 컬렉션 생성
> db.createCollection("myCollection")

# 등록된 컬렉션 조회 가능
> db.showCollections
```

## 2.3 MongoDB에 저장할 데이터 Web Crowling

- 타겟 크롤링 페이지 선정

[시외버스터미널 시간표 및 예매 요금 정보](https://bus.koreacharts.com/intercity-bus-terminal.html)

- Python 크롤링 코드 작성

```python
import requests
from bs4 import BeautifulSoup
import json

url = 'https://bus.koreacharts.com/intercity-bus-terminal.html'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

num = 10000

# 크롤링 결과를 저장할 딕셔너리
bus_info_dict = {}

# 첫 번째 <ul> 안의 <a> 태그 크롤링
first_ul = soup.find('ul', class_='list-unstyled')
first_links = first_ul.find_all('a')
iteratorNum = len(first_links)
iteratorNumChk = 0;
for link in first_links:
    key = link.text.strip() # ex. 간성
    value_dict = {} # ex. 간성 : {}

    # 두 번째 <ul> 안의 <a> 태그 크롤링
    second_url = "https://bus.koreacharts.com" +link.get('href')
    second_response = requests.get(second_url)
    second_soup = BeautifulSoup(second_response.content, 'html.parser')

    second_ul = second_soup.find('ul', class_='list-unstyled')
    second_links = second_ul.find_all('a')
    second_value_dict = {} # ex. 동서울 : {}
    for second_link in second_links:
        second_key = second_link.text.strip() # ex. 간성 - 동서울

        # <table> 안의 정보 크롤링
        third_url = "https://bus.koreacharts.com" + second_link.get('href')
        third_response = requests.get(third_url)
        third_soup = BeautifulSoup(third_response.content, 'html.parser')

        table = third_soup.find('table', class_='table table-striped table-bordered dt-responsive nowrap')
        tbody = table.find('tbody')
        rows = tbody.find_all('tr')

        third_value_dict = []

        for row in rows:
            cols = row.find_all('td')
            bus_id = num
            departure_time = cols[0].text.strip()
            arrival_time = cols[1].text.strip()
            bus_grade = cols[2].text.strip()
            cost = cols[3].text.strip()
            num += 1
            iteratorNumChk += 1

            # 정보를 딕셔너리에 저장
            
            third_value_dict.append({       'bus_id' : bus_id,
                                            'departure_time': departure_time,
                                           'arrival_time': arrival_time,
                                           'bus_grade': bus_grade,
                                           'cost': cost})

        # 두 번째 딕셔너리에 저장
        second_value_dict[second_key] = third_value_dict

    bus_info_dict[key] = second_value_dict
    # bus_info_dict.append(value_dict)
    # print("now crowlled data length .."+str(len(bus_info_dict))+" _ : "+str(num))
    # print(bus_info_dict)
    print("%.2f%%" % (iteratorNumChk / iteratorNum * 100.0))

    # # 첫 번째 딕셔너리에 저장
    # bus_info_dict[key] = value_dict

# 결과 출력
print(bus_info_dict)

filename = "test.json"

with open(filename, 'w', encoding='utf-8') as f:
    json.dump(bus_info_dict, f, ensure_ascii=False)
```

## 2.4 MongoDB에 Web Crowling 데이터 저장

- MongoDB에 insert (같은 경로에 .json파일 필요)

```python
import json
from pymongo import MongoClient

def update():

    print("--------------start insert--------------")

    # JSON 파일 경로
    json_file = "./util/data.json"

    #DB연결
    client = MongoClient("몽고DB주소")
    db = client["myDatabase"]
    bus_database = db["myCollectionTwo"]

    # JSON 파일 읽기
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    data_li = list(data)

    data_li2 = list(data[data_li[0]])

    tuned_dict = []

    for i in range(len(data)):
        temp_dict = {"bus_info":{}}
        temp = {data_li[i] : data[data_li[i]]}
        temp_dict["bus_info"] = temp
        tuned_dict.append(temp)

    #DB 삽입 시작
    for i in range(len(data)):

        exec = bus_database.insert_one(tuned_dict[i])

    print("--------------done--------------")
```

# 3. FastAPI 서버 구축

## 3.1 어플리케이션 디렉토리 구성

- 어플리케이션 디렉토리와 테스트코드 디텍토리 준비

![Untitled](https://github.com/metanet-number1-metabus/api-server/assets/65393001/394afa86-e636-43b6-bdc1-dc625c042c36)


## 3.2 FastAPI 서버 코드 작성

- [main.py](http://main.py) (서버의 전반적인 설정들을 담당)

```python
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
```

- bus_controller.py (사용자의 접속에 대한 라우팅을 담당)

```python
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
        return service_instance.get_destination_for_departure_list(decoded_departure)
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
        return service_instance.get_bus_list(decoded_departure,decoded_destination)
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
```

- bus_service.py (컨트롤러의 요청에 따라 데이터베이스에 데이터 요청을 담당)

```python
from config.connection import Database
from util.mongomanager import update
import time

class Service():

    def __init__(self):
        self.conn = Database().get_connection()

    # # function() : 리스트 보여줄 출발지만 출력
    def get_departure_list(self):

        bus_database = self.conn

        result = bus_database.find()
        keys_departure = []

        for document in result:
            keys_departure.extend(list(document.keys())[1:])

        # ['간성', '거제(고현)', '거진', '고령', '고북', '고창', '고흥', '공주', '관산', ...
        if(len(keys_departure)==0):
            print("-------------------now empty---------------------")
            update()
            

        return keys_departure

    # # function(departure) : 리스트 보여줄 위 내용에 대한 목적지 출력
    def get_destination_for_departure_list(self, departure):

        bus_database = self.conn

        search_str = departure
        query = {search_str: {'$exists': True}}
        projection = {search_str: 1}
        result = bus_database.find(query, projection)

        keys_destination = []  # 리스트 초기화 위치 수정

        for document in result:
            keys_destination.extend(list(document[search_str].keys()))

        # ['동서울', '장신리', '속초', '대구동부', '부산동부', '원통', '전주시외터미널']
        return keys_destination

    # # function(departure, destination) : 리스트 보여줄 출발지만 출력
    def get_bus_list(self, departure, destination):

        bus_database = self.conn

        resultTemp = bus_database.find()
        keys_departure = []

        for document in resultTemp:
            keys_departure.extend(list(document.keys())[1:])

        if(len(keys_departure)==0):
            update()

        search_str_departure = departure
        search_str_destination = destination
        query = {search_str_departure: {'$exists': True}}
        projection = {search_str_departure: 1}
        result = bus_database.find(query, projection)

        bus_list = []  # 리스트 초기화 위치 수정

        for document in result:
            bus_list = document[search_str_departure][search_str_destination]

        # {'bus_id': 10000, 'departure_time': '07시40분', 'arrival_time': '10시56분', 'bus_grade': '일반', 'cost': '21,100원'} ...
        return bus_list
```

- bus_connection.py (데이터베이스와 연결을 담당)

```python
# connection.py
from pymongo import MongoClient

class Database():

    def __init__(self):
        self.client = MongoClient("몽고DB주소")
        self.db = "myDatabase"
        self.collection = "myCollectionTwo"
    
    def get_connection(self):
        client = self.client
        db = client[self.db]
        database_collection = db[self.collection]

        return database_collection
```

## 3.3 FastAPI 테스트 코드 작성

- Pytest를 수행한 결과에 따른 Coverage 결과

![image](https://github.com/metanet-number1-metabus/api-server/assets/65393001/56349ed1-8c22-459d-b864-f86364dda03d)


# 4. 배포

## 3.1 FastAPI 서버 & MongoDB 서버 배포

- docker-compose.yml 파일을 사용해 배포

```yaml
version: "3"

services:
  api:
    build: .
    image: bus-api
    container_name: myfastapi
    ports:
      - "8888:8000"
      - "8443:8443"
    restart: always
    env_file:
      - .env.prod
    depends_on:
      - database
    volumes:
      - /etc/letsencrypt:/ssl
  
  database:
    image: mongo:5.0.15
    container_name: mymongo
    ports:
      - "몽고포트:몽고포트"
    restart: always
    volumes:
      - ./mongodbvol:/data/db

volumes:
  data:
```
 
## Issue

  0. sudo docker-compose down, sudo docker-compose build --no-cache, sudo docker-compose up -d, sudo docker system prune, sudo docker image prune, sudo docker container prune, sudo docker image rm -f [컨테이너ID]
  1. sudo docker build --no-cache -t bus-api .
  2. sudo docker-compose up -d
  3. sudo docker logs [컨테이너ID]
  4. sudo docker exec -it mymongo bash
    - 몽고DB 기본 사용명령: https://freekim.tistory.com/13

  5.volumes 섹션에서 data 볼륨을 정의하고 있다. 이 볼륨은 MongoDB 컨테이너 내부의 /data/db 경로와 호스트의 /var/lib/docker/volumes/프로젝트명_data/_data 경로를 연결합니다. 즉, MongoDB 컨테이너의 데이터가 호스트 compose파일 경로의 mongodbvol 볼륨에 저장됩니다. 
    volumes:
      - ./mongodbvol:/data/db
  6.CORS (Cross-Origin Resource Sharing) 정책에 의해 발생하는 것입니다. 이 오류는 보안 상의 이유로 인해 웹 브라우저에서 동일한 출처가 아닌 서버로의 AJAX 요청을 차단하는 정책 해결해야댐
