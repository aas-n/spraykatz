# [```SPRAYKATZ```](https://github.com/aas-n/spraykatz/blob/master/README.md)
A tool to spray love around the world by [@lydericlefebvre](https://twitter.com/lydericlefebvre).

### Index

| Title        | Description   |
| ------------- |:-------------|
| [About](#about)  | Brief Description about the tool. |
| [Installation](#installation)  | Installation and Requirements. |
| [Usage](#using-spraykatz)  | How to use Spraykatz. |
| [Todo](#todo)  | Things planned to improve this tool. |
| [Acknowlegments](#acknowlegments)  | Acknowlegments. |

### About  
Spraykatz is a tool without any pretention able to **retrieve credentials** on large Active Directory networks. It tries to __filelessly procdump__ machines and __parse dumps locally__ in order to **avoid detections** by antivirus softwares as much as possible.

### Installation
This tool is written for **`>= python3.6`**. You have to use python3.6 and pip3.6.
#### Ubuntu
On a fresh updated Ubuntu.
```bash
apt update
apt install -y python3.6 python3-pip git nmap
git clone --recurse-submodules https://github.com/aas-n/spraykatz.git
cd spraykatz
pip3 install -r requirements.txt
```

### Using Spraykatz  

| Switches | Mandatory | Description |
| ------ |:------------|:--------|
| -u, --username | Yes | The user must have admin rights on targeted systems in order to have code execution. |
| -p, --password | Yes | This password can also be a NTLM hash in the `LM:NT` format. |
| -t, --targets | Yes | Targets can be IP addresses or IP addresses ranges. Targets can be submitted via a targets file (one target per line) or inline (separated by commas). |
| -d, --domain | No | If the user is **not** member of a domain, you can use `-d .` of nothing at all. |
| -m, --methods | No | Execution method to use. If omitted, wmiexec is tried first, then atexec, and  then smbexec. |
| -s, --share | No | SMB Share to use for command execution. By default: `C$`. |

A simple example could be:
```bash
./spraykatz.py -d company.local -u H4x0r -p L0c4L4dm1n -t 192.168.1.0/24
```

### TODO
Many things to come:
- [x] Targets file as input
- [ ] Use nmap python
- [ ] Threading
- [ ] Logging
- [ ] Put gif instead of an image in README.md
- [ ] Refactoring code
- [ ] Domadmin features
- [x] Use Impacket as git submodules
- [ ] Implement mmcexec
- [ ] Tests

### Acknowlegments  
Spraykatz uses slighlty modified parts of the following projects:
* [Impacket](https://github.com/SecureAuthCorp/impacket)
* [Pypykatz](https://github.com/skelsec/pypykatz)
* [CrackMapExec](https://github.com/byt3bl33d3r/CrackMapExec)
* [Pywerview](https://github.com/the-useless-one/pywerview)
* [Sysinternals](https://docs.microsoft.com/en-us/sysinternals/downloads/)

# 
*Created by [Lydéric Lefebvre](https://www.linkedin.com/in/lydericlefebvre/)*
