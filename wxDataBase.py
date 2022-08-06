# This program takes city name and pushes weather data to a database
# Scrapes data from web to push to db
import MySQLdb
import requests
from bs4 import BeautifulSoup
from datetime import date

conn = MySQLdb.connect(
    host = 'localhost',
    user = 'root',
    password = 'baodan613',
    database = 'weatherdb'
)

cursor = conn.cursor()
print("Successful connection")

def pushData(city, date, low, high, humidity, cond):
    insertOper = "INSERT INTO {}(Date, DailyLow, DailyHigh, Humidity, `Condition`) VALUES(%s, %s, %s, %s, %s);".format(city.replace(' ', ''))
    data = (date, low, high, humidity, cond)
    try:
        cursor.execute(insertOper, data)
    except MySQLdb.Error as e:
        try:
            cursor.execute("CREATE TABLE {} (Date VARCHAR(255), DailyLow VARCHAR(255), DailyHigh VARCHAR(255), Humidity VARCHAR(255), `Condition` VARCHAR(255));".format(city.replace(' ', '')))
            cursor.execute(insertOper, data)
        except MySQLdb.Error as e:
            return
    conn.commit()
    print("Successfull data commit for ", city, " weather")

def CollectCityWx(name):
    hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    URL = "https://www.google.com/search?q=%s+weather" % name
    r = requests.get(URL, headers = hdrs)
    soup = BeautifulSoup(r.content, 'lxml')

    today = date.today()
    d = today.strftime("%B %d, %Y")
    loc = soup.find("div", {"id": "wob_loc"}).text

    div1 = soup.find("div", {"class": "vk_bk wob-unit"})
    units = div1.find("span", {"aria-label": "°Celsius"}).text
    div2 = soup.find("div", {"class": "wob_dcp"})
    condition = div2.find("span", {"id": "wob_dc"}).text
    div3 = soup.find("div", {"class": "gNCp2e"})
    high = div3.find("span", {"class": "wob_t"}).text
    div4 = soup.find("div", {"class": "QrNVmd ZXCv8e"})
    low = div4.find("span", {"class": "wob_t"}).text
    div5 = soup.find("div", {"class": "wtsRwe"})
    humid = div5.find("span", {"id": "wob_hm"}).text

    sp = loc.split(",")
    loc = sp[0]
    low = low + " " + units
    high = high + " " + units
    print(loc, " weather on ", d, ":", low, high, humid, condition)
    pushData(loc, d, low, high, humid, condition)

def checkIfHasWords(str):
    for i in str:
        if i.isalpha():
            return True
    return False

InputFile = open("/home/pi/project2022/webScraping/cityInput.txt", 'r') # read only
CityList = InputFile.readlines()
for city in CityList:
    if checkIfHasWords(city)==False:
        break
    print(city)
    CollectCityWx(city) # collects, then sends
conn.close()
