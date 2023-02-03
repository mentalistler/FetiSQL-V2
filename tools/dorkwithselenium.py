from selenium import webdriver
import chromedriver_autoinstaller
import geckodriver_autoinstaller
import re
from urllib.parse import urlparse, urlsplit, urlunsplit
from tools import colorprint
arama_motorlari = [
    "http://www.google.com/search?q={Key}&num=100&start=0",
    #"http://www.google.com/search?q={Key}&num=100&start=100",
   # "http://www.google.com/search?q={Key}&num=100&start=200",
    

]

def aramamotoru():
    try:
        driver = webdriver.Firefox()
    except:
        try:
            geckodriver_autoinstaller.install()
            driver = webdriver.Firefox()
        except:
            try:
                driver = webdriver.Chrome()
            except:
                chromedriver_autoinstaller.install()
                driver = webdriver.Chrome()
    durum = 0
    url_list = []
    dorks = open("files/dorks.txt", "r").read().splitlines()
    for h in range(len(arama_motorlari)):
        for u in range(len(dorks)):
                motor = arama_motorlari[h].replace("{Key}",dorks[u])
                driver.get(motor)
                page_source = driver.page_source
                if(page_source.find("captcha")>-1):
                    colorprint.colorprint("Captchayı çözün ardından [Enter] tuşuna basın.","w")
                    a = input()
                pattern = r'<a href="(.*?)"'
                # regex ile hrefleri bul
                matches = re.findall(pattern, page_source)

                # hrefleri ekrana yazdır
                result = open("results/results.txt", "a")
                for match in matches:
                    if(match.find("google")>-1):
                        pass
                    else:
                        if(match.find("http")>-1):
                            url = match.replace("&amp;","&")
                            url_list.append(url)
                            result.write(url+" \n")
    unique_urls = []
    unique_domains = set()
    for url in url_list:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if "http://" + domain not in unique_domains and "https://"+domain not in unique_domains:
            if(url.find("https://")>-1):
                unique_domains.add("https://"+domain)
            else:
                unique_domains.add("http://"+domain)
            unique_urls.append(url)
    if(durum ==1):
        UrlList = unique_domains
    else:
        UrlList = unique_urls
    with open("results/results.txt", "w") as file:
            file.writelines("%s\n" % url for url in UrlList)
    colorprint.colorprint("results/results.txt kaydedildi!")
    driver.quit()
#aramamotoru
