import requests

url = "https://api-cloud-function.elice.io/5a327f26-cc55-45c5-92b7-e909c2df0ba4/v1/chat/completions"

payload = {
    "model": "helpy-pro",
    "sess_id": "test",
    "messages": [
        {
            "content": "너 한국어 가능해?",
            "role": "user"
        }
    ]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3MzExNTc4NTAsIm5iZiI6MTczMTE1Nzg1MCwia2V5X2lkIjoiZTVjOGRhZjktMTljMS00ZTA5LTk2NmQtZWM2ZGVmYmU4MjE5In0.D19RyCm1ktv2I7BrACIcqJix9aIooqntJVrQdQh8w9M"
}

response = requests.post(url, json=payload, headers=headers)

# print(response.text)
print(response.text.choices[0].message.content.strip())