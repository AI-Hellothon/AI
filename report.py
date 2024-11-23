import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
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

output_file = open("response_output.txt", "w", encoding="utf-8")

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
                                    "각 항목은 중복된 내용을 제거하고 관련된 내용만 간결하게 정리해주세요."}
    ]
}

response = requests.post(url, json=payload, headers=headers)

try:
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content'].replace("#", "").replace("*", "").strip()
except (KeyError, IndexError, json.JSONDecodeError):
    answer = "응답 처리 중 오류가 발생했습니다."

# 생성된 보고서를 출력
print("일상 보고서:\n")
print(answer)
output_file.write("일상 보고서:\n\n")
output_file.write(answer)

output_file.close()

print("\n응답이 response_output.txt 파일에 저장되었습니다.")
