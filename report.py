import os
import requests
import json
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
token = os.getenv('ML_API_key')

url = "https://api-cloud-function.elice.io/5a327f26-cc55-45c5-92b7-e909c2df0ba4/v1/chat/completions"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {token}"
}

try:
    with open("content.txt", "r", encoding="utf-8") as input_file:
        user_input = input_file.read().strip()
except FileNotFoundError:
    print("content.txt 파일을 찾을 수 없습니다.")
    user_input = "기본 입력값"

payload = {
    "model": "helpy-pro",
    "sess_id": "test",
    "messages": [
        {"role": "system", "content": "하루 일과에 대한 보고서를 작성해야 합니다."},
        {"role": "user", "content": f"'{user_input}'는 사용자가 입력한 내용입니다.\n"
                                    "다음 5가지 항목으로 내용을 분류해서 작성해주세요:\n"
                                    "1. 일상 생활\n"
                                    "2. 건강 상태\n"
                                    "3. 식습관 및 영양\n"
                                    "4. 취미 및 여가활동\n"
                                    "5. 기타 사항\n"
                                    "각 항목은 중복된 내용을 제거하고 관련된 내용만 간결하게 정리해주세요.\n"
                                    "다른 말은 적지마."}
    ]
}

response = requests.post(url, json=payload, headers=headers)

try:
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content'].replace("#", "").replace("*", "").strip()
    # 응답 데이터를 카테고리별로 분리
    sections = answer.split("\n\n")  # 카테고리별로 나누기 (빈 줄 기준)
    report_data = {
        "life": "",
        "health": "",
        "food": "",
        "hobby": "",
        "etc": ""
    }

    print(report_data)

    for section in sections:
        if section.startswith("1. 일상 생활"):
            report_data["life"] = section.replace("1. 일상 생활", "").strip()
        elif section.startswith("2. 건강 상태"):
            report_data["health"] = section.replace("2. 건강 상태", "").strip()
        elif section.startswith("3. 식습관 및 영양"):
            report_data["food"] = section.replace("3. 식습관 및 영양", "").strip()
        elif section.startswith("4. 취미 및 여가활동"):
            report_data["hobby"] = section.replace("4. 취미 및 여가활동", "").strip()
        elif section.startswith("5. 기타 사항"):
            report_data["etc"] = section.replace("5. 기타 사항", "").strip()

except (KeyError, IndexError, json.JSONDecodeError):
    report_data = {
        "life": "응답 처리 중 오류가 발생했습니다.",
        "health": "",
        "food": "",
        "hobby": "",
        "etc": ""
    }

created_at = datetime.now()

try:
    connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
    cursor = connection.cursor()

    insert_query = """
        INSERT INTO report (life, health, food, hobby, etc, createdAt)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (report_data["life"], report_data["health"], report_data["food"], report_data["hobby"], report_data["etc"], created_at))

    connection.commit()
    print("데이터가 성공적으로 저장되었습니다.")
except mysql.connector.Error as err:
    print(f"데이터베이스 오류: {err}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

output_file = open("response_output.txt", "w", encoding="utf-8")
output_file.write(answer)
output_file.close()

print("응답이 response_output.txt 파일에 저장되었습니다.")

