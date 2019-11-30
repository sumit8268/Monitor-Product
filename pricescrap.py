from bs4 import BeautifulSoup
import re
import requests
import smtplib

def price(url):
    # url = 'https://www.amazon.in/Test-Exclusive-608/dp/B07HGBMJT6/ref=lp_18199393031_1_1?s=electronics&ie=UTF8&qid=1574361148&sr=1-1'


    header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


    page = requests.get(url, headers=header)
    soup = BeautifulSoup(page.content, "html.parser")

    if (re.search("flipkart", url)):
        site = "flipkart"
        title = soup.find(attrs={"class": "_35KyD6"}).get_text()
        price1 = soup.find(attrs={"class": "_1vC4OE _3qQ9m1"}).get_text()
        img = soup.find(attrs={"class": "_2_AcLJ"})
        i = re.findall("https.*", str(img))[0][:-9]
    if(re.search("amazon", url)):
        site = "amazon"
        title = soup.find(id="productTitle").get_text()
        price1 = soup.find(id="priceblock_ourprice").get_text()
         # details = soup.find(id="prodDetails").get_text()
        img = str(soup.find(id="landingImage"))
        i = re.findall("https.*\.jpg",img)[0].split(',')[0][:-6]

    return site, title.strip(), price1, i, url


def sendupdatemail(link, email, pname, pr):
    # link, email, pname, pr = "www.amazon.com", "sumitpatil8247@gmail.com", "pennnnnn", "300"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('pricetag8241@gmail.com', 'wpgltmplahjnrdib')
    subject = f"product {pname} price dropped down to {pr}"
    body = f"Check the link to view the product site {link}"
    msg = f"Price Tag \n\nSubject: {subject}\n\n{body}".encode('utf-8')
    server.sendmail('pricetag8241@gmail.com', email, msg)
    server.quit()


def forgetpassmail(email, code):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('pricetag8241@gmail.com', 'wpgltmplahjnrdib')
    subject = "Change of price tag account password."
    body = "To change your account password type the below mentioned 6 digit code in the new password page you were redirected to."
    msg = f"Price TAG\n\nSubject: {subject}\n\n{body}\nCode: {code}"
    server.sendmail('pricetag8241@gmail.com', email, msg)
    server.quit()


