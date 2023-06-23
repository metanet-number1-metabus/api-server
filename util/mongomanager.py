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
