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

category=['일상 생활', '건강 상태', '식습관 및 영양', '취미 및 여가활동', '기타 사항']

for element in category:
    payload = {
    "model": "helpy-pro",
    "sess_id": "test",
    "messages": [
        {"role": "system", "content": "하루 일과에 대한 보고서를 만들어야돼."},
        {"role": "user","content":  f"'{user_input}'는 사용자가 입력한 내용이야.\n"
                        f"입력된 내용을 정리하고\n"
                        f"{element}관련 내용을 간추려서 적어봐.\n"
                        f"다른말은 적지마.\n"}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

try:
    response_json = response.json()
    answer = response_json['choices'][0]['message']['content'].replace("#", "").replace("*", "").strip()
except (KeyError, IndexError, json.JSONDecodeError):
    answer = "응답 처리 중 오류가 발생했습니다."

output_file.write(f"{answer}\n\n")
output_file.close()

print("응답이 response_output.txt 파일에 저장되었습니다.")

