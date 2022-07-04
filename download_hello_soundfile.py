import requests
KAKAO_SECRET_KEY = '8fe999d88a71611a14ad568513311af8'

headers = {
    #Transfer-Encoding: chunked # 보내는 양을 모를 때 헤더에 포함한다.
    'Host': 'kakaoi-newtone-openapi.kakao.com',
    'Content-Type': 'application/xml',
    'X-DSS-Service': 'DICTATION',
    'Authorization': f'KakaoAK {KAKAO_SECRET_KEY}',
}

data = '''<speak><voice name="MAN_READ_CALM">어서오세요~</voice> </speak>'''
response = requests.post('https://kakaoi-newtone-openapi.kakao.com/v1/synthesize', headers=headers, data=data.encode('utf-8'))
# 요청 URL과 headers, data를 post방식으로 보내준다.

rescode = response.status_code
print(rescode)
if(rescode==200):
    print("TTS mp3 저장")
    response_body = response.content
    with open('./soundfile/hello_kr.mp3', 'wb') as f:
        f.write(response_body)
else:
    print("Error Code:" + rescode)