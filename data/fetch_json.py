import sys

import requests
import json
from requests.exceptions import *

HEADERS = {
    'Content-Type': 'application/json'
}


def fetch(url: str) -> list | dict:
    print(f"{url}에서 데이터 불러오는 중")
    try:
        response = requests.get(url, headers=HEADERS)

        # HTTP 상태 코드 오류 처리
        response.raise_for_status()

        try:
            data = response.json()  # JSON 파싱
        except json.JSONDecodeError as e:
            print("JSON 파싱 실패:", e)
            sys.exit(1)
    except ConnectionError as e:
        print("네트워크 연결 오류:", e)
        sys.exit(1)
    except Timeout as e:
        print("요청 시간 초과:", e)
        sys.exit(1)
    except TooManyRedirects as e:
        print("리다이렉션 횟수 초과:", e)
        sys.exit(1)
    except URLRequired as e:
        print("URL이 잘못됨:", e)
        sys.exit(1)
    except MissingSchema as e:
        print("URL 스키마 누락 (예: http/https):", e)
        sys.exit(1)
    except InvalidSchema as e:
        print("잘못된 스키마:", e)
        sys.exit(1)
    except InvalidURL as e:
        print("잘못된 URL 형식:", e)
        sys.exit(1)
    except HTTPError as e:
        print("HTTP 오류 발생:", e)
        sys.exit(1)
    except RequestException as e:
        # requests 라이브러리에서 발생할 수 있는 모든 예외의 최상위 클래스
        print("요청 중 일반적인 오류:", e)
        sys.exit(1)
    except Exception as e:
        # 파이썬의 모든 예외 처리 (예상 못한 오류 대비)
        print("알 수 없는 오류 발생:", e)
        sys.exit(1)
    print(f"{url}에서 데이터 불러오기 완료")
    return data
