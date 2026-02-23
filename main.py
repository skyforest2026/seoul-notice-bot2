import requests
from bs4 import BeautifulSoup
import time
import os

# GitHub Secrets에서 정보를 가져오도록 설정 (보안상 중요)
TELEGRAM_TOKEN = os.environ.get('AAGMhP8dyOJnpVPGo9Y4qBOk3OgTe5qddjQ')
CHAT_ID = os.environ.get('7478800309')
KEYWORDS = ["연번동의서", "재개발", "재건축"]

DISTRICTS = {
    "강남구": "https://www.gangnam.go.kr/office/gigo/list.do",
    "강동구": "https://www.gangdong.go.kr/web/portal/ko/bbs/list.do?bbsId=00001",
    "강북구": "https://www.gangbuk.go.kr/www/board/list.do?bbsId=B0001",
    "강서구":	"https://www.gangseong.go.kr/gs010101",
    "관악구":"	https://www.gwanak.go.kr/site/gwanak/ex/bbs/List.do?cbIdx=239",
    "광진구":	"https://www.gwangjin.go.kr/portal/bbs/B0000001/list.do?menuNo=200191",
    "구로구":	"https://www.guro.go.kr/www/selectBbsNttList.do?bbsNo=655",
    "금천구":	"https://www.geumcheon.go.kr/portal/selectBbsNttList.do?bbsNo=150",
    "노원구":	"https://www.nowon.kr/www/user/bbs/BD_selectBbsList.do?q_bbsCode=1007",
    "도봉구":	"https://www.dobong.go.kr/bbs.asp?b_code=10001",
    "동대문구":	"https://www.ddm.go.kr/www/selectBbsNttList.do?bbsNo=38",
    "동작구": "https://www.dongjak.go.kr/portal/main/contents.do?menuNo=200045",
    "마포구":	"https://www.mapo.go.kr/site/main/board/gosi",
    "서대문구":	"https://www.sdm.go.kr/news/notice/notice.do",
    "서초구":	"https://www.seocho.go.kr/site/seocho/ex/bbs/List.do?cbIdx=247",
    "성동구":	"https://www.sd.go.kr/main/selectBbsNttList.do?bbsNo=183",
    "성북구":	"https://www.sb.go.kr/main/selectBbsNttList.do?bbsNo=4",
    "송파구":	"https://www.songpa.go.kr/e_gov/selectBbsNttList.do?bbsNo=81",
    "양천구":	"https://www.yangcheon.go.kr/site/yangcheon/ex/bbs/List.do?cbIdx=261",
    "영등포구":	"https://www.ydp.go.kr/www/selectBbsNttList.do?bbsNo=34",
    "용산구":	"https://www.yongsan.go.kr/portal/main/contents.do?menuNo=200018",
    "은평구":	"https://www.ep.go.kr/www/selectBbsNttList.do?bbsNo=52",
    "종로구":	"https://www.jongno.go.kr/portal/bbs/B0000002/list.do?menuNo=200057",
    "중구":	"https://www.junggu.seoul.kr/board/B0002/list.do?menuNo=200451",
    "중랑구":	"https://www.jungnang.go.kr/portal/bbs/B0000001/list.do?menuNo=200469"
}

def check_notices():
    found_list = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    for name, url in DISTRICTS.items():
        try:
            res = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all(['a', 'td']) # 제목이 있을 법한 태그들
            
            for link in links:
                text = link.get_text().strip()
                if any(kw in text for kw in KEYWORDS):
                    found_list.append(f"📍 {name}: {text}\n🔗 {url}")
                    break # 한 구청에서 하나라도 찾으면 일단 추가 (중복 방지)
            time.sleep(1)
        except:
            continue
    return found_list

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

new_notices = check_notices()

if not new_notices:
    send_telegram("❌ 특이사항 없음")
else:
    report = "🚨 [긴급] 신규 공고 발견!\n\n" + "\n\n".join(new_notices)
    send_telegram(report)
