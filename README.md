auto-discover
=============

A network discovery tool that uses nmap to identify if ssh,ping, and snmp are running on
various connected devices in a network.

Installation
============

```pip install https://github.com/thomasvincent/python-auto-discover/tarball/master```


Usage
=====

Usage: auto-discover <ip-address>
Examples:
auto-discover 10.73.19.0
    
   

Output
======
The tool outputs a CSV file named `devices.csv` with the following columns:

| Host | IP | SNMP Group | Alive | SNMP | SSH | MySQL | Username |
|------|----|------------|-------|------|-----|-------|----------|
| ...  | ...| ...        | ...   | ...  | ... | ...   | ...      |


