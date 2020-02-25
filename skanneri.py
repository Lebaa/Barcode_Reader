import xlrd
import os.path
from xlutils.copy import copy
import sys
import datetime
from evdev import InputDevice, categorize, ecodes
from selenium import webdriver
import time
import secret
from emailer import emailer


#Funktio jolla avataan selaimeen tilausta vastaava ticketti serviceNowsta
def selain(ritm):
    driver = webdriver.Firefox()
    driver.get("https://idp.jyu.fi/nidp/saml2/sso?id=jyu&sid=0&option=credential&sid=0")
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/fieldset/form/div[1]/div/input").send_keys(secret.usr)
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div/fieldset/form/div[2]/div/input").send_keys(secret.pwd)
    driver.find_element_by_xpath('//*[@id="login-submit1"]').click()
    time.sleep(2)
    driver.get(("https://help.jyu.fi/text_search_exact_match.do?sysparm_search=")+ritm)

#Viivakoodilukija antaa tiedon HID muodossa, käännetään se oikeiksi numeroiksi
def HIDconverter(i):
    if i == 30:
        return 1
    if i == 31:
        return 2
    if i == 32:
        return 3
    if i == 33:
        return 4
    if i == 34:
        return 5
    if i == 35:
        return 6
    if i == 36:
        return 7
    if i == 37:
        return 8
    if i == 38:
        return 9
    if i == 39:
        return 0

tilausnumero = ""

fp = open("/dev/barcode","rb")

#Kuunnellaan jatkuvasti koska tulee viivakoodia, nollista ei tarvitse välittää, 40 on taas normaalina inputtina 40 joten siihen lopetetaan
while True:
    buffer = fp.read(32)
    for c in buffer:
        if 0<c:
            if c <40:
                tilausnumero = tilausnumero + str(HIDconverter(c))
            elif c == 40:
                print("break")
                break

#Excelin avaus sälää, polku ja kopio sheetistä
    polku = '/home/lehmik/Documents/testi.xlsx'
    filu = xlrd.open_workbook(os.path.join(polku))
    p = filu.sheet_names()
    wb = copy(filu)
    wb_sheet = wb.get_sheet(0)
#Haetaan excelistä löytyykö viivakoodia vastaavaa tilausnumeroa, jos löytyy potkaistaan yläällä oleva selainfunktio, erillisenä oleva sähköpostin lähetys ja
#exceliin kirjoitus käyntiin. Lopputuloksena exceliin päivittyy tilauksen saapumispäivä, selain avaa tilausta vastaavan tiketin ja lähetetään maili asiasta asiakkaalle.
    for y in p:
        sh = filu.sheet_by_name(y)
        for rownum in range(sh.nrows):
          if rownum != 0:
            if int(tilausnumero) == int(sh.row_values(rownum)[2]):
                date = str(datetime.date.today().day) + "." + str(datetime.date.today().month) + "." + str(datetime.date.today().year)
                wb_sheet.write(rownum,5,date)
                wb.save(os.path.join(polku))
                selain(str(sh.row_values(rownum)[3]))
                emailer("Tietokoneen saapumisilmoitus","Tilauksesi on saapunut,asennellaan kun keritään",secret.email, secret.emailpwd, "mika.lehtinen92@gmail.com")

















