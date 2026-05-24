# mypreparations

Personal automation toolkit for OSCP & OSEP lab/exam use.

By ardias

---

## Structure

```
mypreparations/
├── OSCP/   — scripts for OSCP labs
└── OSEP/   — scripts for OSEP labs
```

---

## OSCP

Lightweight scripts for OSCP workflow.

| Script | Usage | Description |
|--------|-------|-------------|
| `aunmap` | `aunmap <ip> [--udp]` | Auto nmap: full port → sCV → UDP. Parallel, resume support |
| `create` | `create <name>` | Create new lab note/directory structure |
| `ph` | `ph` | Pentest helper quick ref |
| `phs` | `phs [topic]` | Pentest cheatsheet |
| `sl` | `sl <ip>` | Quick service lookup |
| `sw` | `sw <ip>` | Switch target IP |
| `tf_generate` | `tf_generate` | Generate file transfer one-liners |

Install:
```bash
cp OSCP/* /usr/local/bin/ && chmod +x /usr/local/bin/{aunmap,create,ph,phs,sl,sw,tf_generate}
```

---

## OSEP

Full automation toolkit for OSEP — AD attacks, lateral movement, tunneling, payloads.

| Script | Usage | Description |
|--------|-------|-------------|
| `aunmap` | `aunmap <ip> [--udp]` | Port discovery via rustscan → nmap sCV. Parallel multi-target, resume support |
| `smbenum` | `smbenum <ip> [user] [pass]` | SMB enum via nxc |
| `adenum` | `adenum <dc_ip> <domain> <user> <pass>` | Kerberoast + AS-REP + BloodHound |
| `adcsenum` | `adcsenum <dc_ip> <domain> <user> <pass>` | ADCS ESC1/4/8 enum + exploit commands |
| `lapsread` | `lapsread <dc_ip> <domain> <user> <pass>` | Dump LAPS + GPP creds |
| `crack` | `crack <hash_file> [wordlist]` | Auto-detect hash → hashcat |
| `spray` | `spray <target> <user> <pass\|hash> [proto]` | Credential spray across protocols |
| `dcsync` | `dcsync <dc_ip> <domain> <user> <pass\|hash>` | DCSync → ntds_raw.txt + ntds_nt.txt |
| `pth` | `pth <target\|cidr> <user> <hash>` | Pass-the-Hash, CIDR sweep |
| `mssqlshell` | `mssqlshell <target> <user> <pass\|hash>` | MSSQL shell via xp_cmdshell |
| `ligolo` | `ligolo <kali_ip> <port> <subnet>` | Ligolo-ng tunnel setup |
| `serve` | `serve [path] [port] [--upload] [--ssl]` | HTTP file server |
| `loot` | `loot <file> <output> [port]` | File transfer one-liners |
| `genpayload` | `genpayload <lhost> <lport> [platform]` | msfvenom wrapper |
| `msfshell` | `msfshell <lhost> <lport> [platform]` | MSF multi/handler |
| `hoaxshell` | `hoaxshell <lhost> [port] [--ssl]` | Obfuscated PS reverse shell |
| `qhelp` | `qhelp [topic]` | Inline cheatsheet |
| `toolkit` | `toolkit` | Full script reference + attack flow |

Install:
```bash
cd OSEP && sudo bash install
```

Requires `~/.servepaths` for `serve`:
```bash
LINUX_TOOLS=/path/to/linux/tools
WINDOWS_TOOLS=/path/to/windows/tools
```
