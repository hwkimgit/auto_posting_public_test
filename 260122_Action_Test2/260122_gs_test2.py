import gspread
import json
import os
import datetime
from oauth2client.service_account import ServiceAccountCredentials

# 1. GitHub 금고(Secret)에 저장한 JSON 열쇠를 로봇이 꺼내옵니다.
secret_json = os.environ.get('GSPREAD_AUTH')
auth_info = json.loads(secret_json)

# 2. 접속 권한(Scope) 설정
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(auth_info, scope)
client = gspread.authorize(creds)

# 3. 구글 시트 열기 (공유 설정한 시트 이름과 정확히 일치해야 합니다)
# 아까 만드신 시트 이름인 '260122_Action_Test'를 입력하세요.
spreadsheet = client.open("260122_Action_Test")
sheet = spreadsheet.worksheet("test_시트2") # 하단 탭 이름

# 추가 : 기록시간(현재 시간 포함)
# 한국 시간은 UTC보다 9시간 빠르므로timedelta를 더해줍니다.
now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
now_str = now.strftime('%Y-%m-%d %H:%M:%S')

#추가 : 실행 원인 파악하기(수동, 스케쥴 등)
event_name = os.environ.get('RUN_TYPE', 'unknown')
if event_name == 'workflow_dispatch':
    run_mode = "수동 실행"
elif event_name == 'schedule':
    run_mode = "스케쥴 실행"
else:
    run_mode = f"기타 ({event_name})"

# 4. 데이터 추가하기
data = [
    ["첫 번째 로봇", "성공적으로 접속했습니다!", now_str, run_mode],
]

for row in data:
    sheet.append_row(row)

print("✅ 구글 시트에 데이터 저장을 완료했습니다!")
