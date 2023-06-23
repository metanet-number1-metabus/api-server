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


from main import app
from model.bus_service import Service

def test_get_departure_list():
    service = Service()
    buses = service.get_departure_list()
    assert len(buses) > 0
    # Add more assertions based on the expected result

def test_get_destination_for_departure_list():
    testQuery = "거제(고현)"
    service = Service()
    buses = service.get_destination_for_departure_list(testQuery)
    assert len(buses) > 0
    # Add more assertions based on the expected result

def test_get_bus_list():
    testQuery = "거제(고현)"
    testQuery2 = "서울남부"
    service = Service()
    buses = service.get_bus_list(testQuery, testQuery2)
    assert len(buses) > 0
    # Add more assertions based on the expected result

# Add more test cases for other methods in bus_service.py
