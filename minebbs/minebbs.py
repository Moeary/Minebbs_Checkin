import requests
from bs4 import BeautifulSoup
import sys

def minebbs(cookie_string):
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': 'https://www.minebbs.com/',
        'Cookie': cookie_string
    }

    try:
        res = session.get("https://www.minebbs.com/", headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        pd = soup.find_all('span', class_="p-navgroup-linkText")
        account = pd[0].text.strip()
        if account == '登录':
            print("Cookie未填或过期！")
        else:
            print("Cookie有效！")
            find_button = soup.find('form', class_="block")
            if find_button:
                xfToken = find_button.find('input', {'name': '_xfToken'})['value']
                data = {'_xfToken': xfToken}
                sign_response = session.post("https://www.minebbs.com/credits/clock", headers=headers, data=data)
                if sign_response.status_code == 200:
                    print("签到成功！")
                else:
                    print(f"签到失败，状态码：{sign_response.status_code}")
            else:
                print("未找到签到按钮，可能已经签到。")

        fid = soup.find_all('dl', class_="pairs pairs--justified fauxBlockLink")
        gold = fid[0].text.strip()
        dia = fid[1].text.strip()
        print(f"金币: {gold}, 钻石: {dia}")

    except requests.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")

if __name__ == "__main__":
    cookie_string = sys.argv[1]
    assert cookie_string
    
    minebbs(cookie_string)