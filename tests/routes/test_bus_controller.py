import sys
import os

# 현재 파일의 경로
current_dir = os.path.dirname(os.path.abspath(__file__))
# 상위 디렉토리의 경로
parent_dir = os.path.dirname(current_dir)
# 상위의 상위 디렉토리의 경로
grandparent_dir = os.path.dirname(parent_dir)

# 상위 디렉토리를 sys.path에 추가합니다.
sys.path.insert(0, grandparent_dir)

# from main import app
from fastapi.testclient import TestClient
from routes.bus_controller import bus_router

client = TestClient(bus_router)

def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello! Our Metabus OpenAPI Service ."
    # Add more assertions based on the expected response

def test_departure_list():
    response = client.get("/get_departure_list")
    assert response.status_code == 200
    assert response.json() == ["간성","거제(고현)","거진","고령","고북","고창","고흥","공주","관산","광명","광주(유·스퀘어)","교통대학","구미","군북","금산","기지시","길음(도심공항)","김제","김포공항(도심공항)","김해","김해공항(세인)국제","김해공항(태화)국제","나주","나주혁신도시","내포시","녹동","논산","당진","대구서부","대전복합","대전서남부","대진","동광양","동서울","동송","마산","마산남부","마산역(리무진)","만리포","목포","무안","무주","문막","문장","배방정류소","백운","북청주","사천","삼성(대소)","삼척","삼천포","삽교천","상주","서산","서수원","서울남부","성남","성전","속초","수락터미널(도심공항)","수안보","수원터미널","순창","순천","순천역","신태인","신평","쏠비치 진도","아산(온양)","안면도","안산터미널","안중","양구","양덕원","양양","여수","여주","여천","영광","영월","영주","영천","영해","예천","오산","옥과","온정","와수리","완도","용궁","용문","용원(녹산,명지)","운산","울산(태화)","울진","원주","원통","유성","율량성모병원","음암","의령","의정부","이천","인제","인천","인천공항2터미널","임자(대광)","잠실역","장수","장흥","전남인재개발원","전주(리무진터미널)","정읍","제주종합","주문진","진도","창원","천안","청송","청주","청주공항","충주","코리아텍","코엑스(도심공항)","태안","평창","평택","하동","한서대","함안","합덕","합천","해남","해미","해인사","현리(강원)","호산","홍천","화순","후포","흥덕"]
    # Add more assertions based on the expected response

def test_destination_list():
    testQuery = "거제(고현)"
    response = client.get("/get_destination_list?departure="+testQuery)
    assert response.status_code == 200
    assert response.json() == ["서울남부","부산서부(사상)","장목","대구동부","통영터미널","대전복합","김해공항","용원(녹산,명지)","진해","마산남부","무전동","김해외고(율하)","창원","구미","인천","동서울","평택","세종시"]

def test_bus_list():
    testQuery = "거제(고현)"
    testQuery2 = "서울남부"
    response = client.get("/get_bus_list?departure="+testQuery+"&destination="+testQuery2)
    assert response.status_code == 200
    assert response.json() == [{"bus_id":10021,"departure_time":"05시40분","arrival_time":"10시00분","bus_grade":"우등","cost":"36,900원"},{"bus_id":10022,"departure_time":"06시20분","arrival_time":"10시40분","bus_grade":"우등","cost":"36,900원"},{"bus_id":10023,"departure_time":"07시00분","arrival_time":"11시20분","bus_grade":"일반","cost":"33,000원"},{"bus_id":10024,"departure_time":"07시40분","arrival_time":"12시00분","bus_grade":"프리미엄","cost":"44,800원"},{"bus_id":10025,"departure_time":"12시00분","arrival_time":"16시20분","bus_grade":"프리미엄","cost":"44,800원"},{"bus_id":10026,"departure_time":"14시00분","arrival_time":"18시20분","bus_grade":"프리미엄","cost":"44,800원"},{"bus_id":10027,"departure_time":"15시00분","arrival_time":"19시20분","bus_grade":"우등","cost":"36,900원"},{"bus_id":10028,"departure_time":"16시00분","arrival_time":"20시20분","bus_grade":"프리미엄","cost":"44,800원"},{"bus_id":10029,"departure_time":"17시00분","arrival_time":"21시20분","bus_grade":"우등","cost":"36,900원"},{"bus_id":10030,"departure_time":"18시00분","arrival_time":"22시20분","bus_grade":"프리미엄","cost":"44,800원"},{"bus_id":10031,"departure_time":"19시20분","arrival_time":"23시40분","bus_grade":"우등","cost":"36,900원"},{"bus_id":10032,"departure_time":"22시00분","arrival_time":"02시20분","bus_grade":"심야프리","cost":"49,300원"}]
    # Add more assertions based on the expected response

# Add more test cases for other API endpoints in bus_controller.py
