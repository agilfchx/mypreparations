# OSEP Toolkit

Personal automation scripts for lab use. 

By ardias

## Install

```bash
cd /path/to/updated/
sudo bash install
```

Installs all scripts to `/usr/local/bin` — run from anywhere after.

---

## Configuration — `~/.servepaths`

Required for `serve` script to know where your tools are:

```bash
LINUX_TOOLS=/path/to/linux/tools
WINDOWS_TOOLS=/path/to/windows/tools
```

`serve` auto-creates this file on first run and prompts you to fill it in.

---

## Scripts

### Recon
| Script | Usage | Description |
|--------|-------|-------------|
| `aunmap` | `aunmap <ip> [--udp]` | Auto nmap: full port → sCV → UDP. Parallel multi-target, resume support |
| `smbenum` | `smbenum <ip> [user] [pass]` | SMB enum via nxc: shares, users, groups, pass-pol, RID brute |

### File Transfer & Serving
| Script | Usage | Description |
|--------|-------|-------------|
| `serve` | `serve [path] [port] [--upload] [--ssl]` | HTTP server — current dir, linux/windows tools dir, or upload mode |
| `loot` | `loot <file> <output> [port]` | Generate file transfer one-liners (certutil, iwr, wget, curl, SMB) |

### AD Enumeration
| Script | Usage | Description |
|--------|-------|-------------|
| `adenum` | `adenum <dc_ip> <domain> <user> <pass>` | Kerberoast + AS-REP roast + BloodHound collection |
| `adcsenum` | `adcsenum <dc_ip> <domain> <user> <pass>` | ADCS enum — finds ESC1/ESC4/ESC8 + prints exploit commands |
| `lapsread` | `lapsread <dc_ip> <domain> <user> <pass>` | Dump LAPS passwords + GPP cached credentials |

### Credential Attacks
| Script | Usage | Description |
|--------|-------|-------------|
| `crack` | `crack <hash_file> [wordlist]` | Auto-detect hash type → hashcat with rockyou + best64 |
| `spray` | `spray <target> <user> <pass\|hash> [--local-auth] [--smb\|--winrm\|--mssql\|--ldap\|--rdp]` | Credential/hash spray across protocols |
| `dcsync` | `dcsync <dc_ip> <domain> <user> <pass\|hash>` | DCSync via nxc → fallback secretsdump. Saves ntds_raw.txt + ntds_nt.txt |

### Lateral Movement
| Script | Usage | Description |
|--------|-------|-------------|
| `pth` | `pth <target\|cidr> <user> <hash> [--local-auth]` | Pass-the-Hash: auto-detect open port → evil-winrm / psexec / wmiexec. CIDR sweep supported |
| `mssqlshell` | `mssqlshell <target> <user> <pass\|hash> [cmd]` | MSSQL: validate → enable xp_cmdshell → interactive or single command |

### Tunneling
| Script | Usage | Description |
|--------|-------|-------------|
| `ligolo` | `ligolo <kali_ip> <port> <internal_subnet>` | Ligolo-ng setup: tun interface + route + print victim command + start proxy |

### Payload Generation
| Script | Usage | Description |
|--------|-------|-------------|
| `genpayload` | `genpayload <lhost> <lport> [platform] [--shell]` | msfvenom wrapper — staged (meterpreter) or stageless (nc-compatible) |
| `msfshell` | `msfshell <lhost> <lport> [platform]` | MSF multi/handler — windows/linux/ps1 |
| `hoaxshell` | `hoaxshell <lhost> [port] [--ssl]` | Obfuscated PS reverse shell (AMSI bypass), auto-start listener |

### Reference
| Script | Usage | Description |
|--------|-------|-------------|
| `toolkit` | `toolkit` | Full usage reference for all scripts + attack flow cheatsheet |
| `qhelp` | `qhelp [topic]` | Inline cheatsheet — `qhelp` lists all topics, `qhelp <topic>` shows commands |

---

## qhelp Topics

```
── Recon ──────────────────
nmap  smb  ldap  dns  snmp  web

── Services ───────────────
ftp  rdp  mysql  mssql  kerberos

── Credentials ────────────
mimikatz  lsass  sam  laps  hash  crack  spray

── Active Directory ────────
bloodhound  kerberoast  asrep  dacl  delegation
dcsync  golden  rbcd  adcs  pth  relay

── Lateral Movement ────────
winrm  wmi  rdp  ssh

── Tunneling ───────────────
ligolo  chisel  ssh

── Privilege Escalation ────
privesc  privesc-win  potato  sudo  suid

── Payloads & Evasion ──────
msfvenom  amsi  applocker  injection  shellcode  rust

── File Transfer ───────────
transfer

── Persistence ─────────────
persist

── Shells ──────────────────
shell  hoaxshell  phishing

── C2 ──────────────────────
c2  msf
```

---