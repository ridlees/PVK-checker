# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import os

def SendAlert():
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    msg = MIMEMultipart()
    #hide the login, password and address
    login, password = 'email','password' #of a random Gmail, so you can send the messages
    msg['Subject'] = 'Alert - Waterbroke'
    msg['From'] = "Alertbot"
    msg['To'] = 'Email'  #the notification email
    msg.preamble = 'Alert - Waterbroke'
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    try:
        s.login(login, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    finally:
        s.quit()


def ScrapPVKAjax(url,headers,Address):
    page = requests.get(url, headers=headers)
    soup= BeautifulSoup(page.content, 'html.parser')
    lisT = soup.findAll("p", {"class": "list"})
    if  lisT[0].text.find(Address) != -1:
        SendAlert()

def ScrapPVK(Address):
    URL = "https://www.pvk.cz/aktuality/havarie-vody/aktualni-havarie/"
    subURL = "https://www.pvk.cz"
    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0'}

    page = requests.get(URL, headers=headers)
    soup= BeautifulSoup(page.content, 'html.parser')
    rows = soup.findAll("div", {"class": "hrow"})
    
    ''' Input example
    <div class="hrow">
    <div class="hcol hcol-s">Praha-Lysolaje<span class="hnoweb hyesmob">, </span></div>
    <div class="hcol hcol-s">Lysolaje<span class="hnoweb hyesmob">, </span></div>
    <div class="hcol hcol-s">Lysolajské údolí 92/68</div>
    <div class="hcol"><strong class="hnoweb hyesmob">Přehled výluk zásobování: </strong>-</div>
    <div class="hcol"><strong class="hnoweb hyesmob">Přehled náhradního zásobování: </strong>-</div>
    <div class="hcol hsm"><strong class="hnoweb hyesmob">Upřesnění: </strong>předpoklad do 15:00</div>
    </div>
    '''
    
    for row in rows[1:len(rows)]:
        a = row.findAll("div", {"class": "hcol"})[3].findAll("a")
        try:
            link = a[0].get("href")
            url = subURL + link
            ScrapPVKAjax(url,headers,Address)
        except:
            print("")
            
        if row.text.find(Address) != -1:
            SendAlert()
            
if __name__ == "__main__":
    
        
    ScrapPVK("Your Address") #set this to your prague address
    
