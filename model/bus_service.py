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



