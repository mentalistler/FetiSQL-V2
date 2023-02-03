import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import threading
import ftplib

from tools import useragent
from tools import colorprint
PanelFound = []

def check_ftp_port(host):
    try:
        ftp = ftplib.FTP(host,timeout=3)
        ftp.quit()
        return True
    except ftplib.all_errors as e:
        return False
def panel_check(url,panels):
    global PanelFound
    durum = 0
    
    for panel in panels:
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            if(panel.find("{}.")):
                domain = domain.replace("www.","")
                panelcheck = panel.replace("{}",domain)
            else:
                panelcheck = panel.replace("{}",domain)
            if(url.find("https://")>-1):
                try:
                    panelcheck = "https://"+panelcheck
                except:
                    panelcheck = "https://"+panelcheck
            else:
                    panelcheck = "http://"+panelcheck
            user_agent = {'User-agent': useragent.get_useragent()}
            response = requests.get(panelcheck,headers=user_agent, timeout=10)
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            forms = soup.find_all('form')
            if forms:
                ftp_status = str(check_ftp_port(domain))
                colorprint.colorprint(f"{url} | {panelcheck} | {ftp_status}")
                PanelFound.append(f"{url} | {panelcheck} | {ftp_status}")
                durum =1
                break
        except:       
            pass
    if(durum ==0):
        ftp_status = str(check_ftp_port(domain))
        colorprint.colorprint(f"{url} | - | {ftp_status}")
        PanelFound.append(f"{url} | - | {ftp_status}")

def main(_type,thread=50):
    global PanelFound
    PanelFound= []
    sql = open("results/sql.txt", "r").read().splitlines()
    if(_type==0):
        panels = open("files/panels.txt", "r").read().splitlines()
    else:
        panels = open("files/quickpanel.txt", "r").read().splitlines()

    threads = []
    i = 0
    while(i < len(sql)):
        for j in range(i,min(i+thread,len(sql))):
            try:
                t = threading.Thread(target=panel_check,args=(sql[j],panels))
                threads.append(t)
                t.start()
            except:
                pass
        for t in threads:
            t.join()
        i += thread
        threads = []
    with open("results/SqlAndPanels.txt", "w") as file:
            file.writelines("%s\n" % url for url in PanelFound)
    colorprint.colorprint("results/SqlAndPanels.txt kaydedildi!")