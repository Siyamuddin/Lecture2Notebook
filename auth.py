import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
TIMEOUT = 3


def get_student_info(student_id: str, password: str):
    print(f"Student authentication started")
    login_data = {
        "email": student_id,
        "password": password
    }

    with requests.Session() as session:
        session.post("https://do.sejong.ac.kr/ko/process/member/login", headers=headers, data=login_data, timeout=TIMEOUT)
        response = session.get("https://do.sejong.ac.kr/", timeout=TIMEOUT)

        soup = BeautifulSoup(response.text, "html.parser")

        info_box = soup.select_one("div.info")
        if not info_box:
            return None

        name = info_box.find("b").get_text(strip=True)
        department = info_box.find('span', class_='institution').string
        major = info_box.find('span', class_='department').string


        return {
            "name": name,
            "department": department,
            "major": major
        }
