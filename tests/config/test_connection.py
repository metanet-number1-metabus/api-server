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
from config.connection import Database

testDB = Database()

def test_get_connection():

    client = testDB.client
    db = client[testDB.db]
    database_collection = db[testDB.collection]
    assert database_collection is not None
    # Add more assertions to test the database connection and operations
