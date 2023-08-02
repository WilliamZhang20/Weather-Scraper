# This program takes city name and pushes weather data to a database
# Scrapes data from web to push to db
import MySQLdb  # Integrated Python with MySQL (https://pynative.com/python-mysql-database-connection/)
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv # used to fetch environment variables
from datetime import date # date important for each weather data point

load_dotenv() # fetch username and password environment vars

mysql_username = os.getenv('mysql_username')
mysql_password = os.getenv('mysql_password')
city_input_directory = os.getenv('city_input_directory')

conn = MySQLdb.connect(
    host = 'localhost',
    user = mysql_username,
    password = mysql_password,
    database = 'weatherdb'
)

cursor = conn.cursor()
print("Successful connection") # Confirmation of connection

def pushData(city, date, low, high, humidity, cond):
    insertOper = "INSERT INTO {}(Date, DailyLow, DailyHigh, Humidity, `Condition`) VALUES(%s, %s, %s, %s, %s);".format(city.replace(' ', ''))
    data = (date, low, high, humidity, cond)
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (Date VARCHAR(255), DailyLow VARCHAR(255), DailyHigh VARCHAR(255), Humidity VARCHAR(255), `Condition` VARCHAR(255));".format(city.replace(' ', ''))) # If table exists, nothing happens.
        cursor.execute("SELECT * FROM {};".format(city.replace(' ', '')))
        res = cursor.fetchall()
        for row in res:  # if there is already a point for today's date, then nothing will be entered
            if row[0]==date:
                conn.commit()
                print('There is already data for ', city, '\'s weather today.\n', sep = '')
                return
        cursor.execute(insertOper, data)
    except MySQLdb.Error as e:
        print("") # newline
        return # does nothing if it doesn't work
    conn.commit()
    print("Successfull data commit for ", city, " weather")
    print("") # newline

def CollectCityWx(name):
    hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
    URL = "https://www.google.com/search?q=%s+weather" % name
    r = requests.get(URL, headers = hdrs)
    soup = BeautifulSoup(r.content, 'lxml')

    today = date.today()
    d = today.strftime("%B %d, %Y")
    loc1 = soup.find("span", {"class": "BBwThe"}).text
    loc2 = soup.find("div", {"id": "wob_loc"}).text
    if loc2 == 'Weather':
        loc = loc1
    else:
        loc = loc2

    div1 = soup.find("div", {"class": "vk_bk wob-unit"})
    units = div1.find("span", {"aria-label": "°Celsius"}).text

    div2 = soup.find("div", {"class": "DxhUm"})
    condIcon = div2.find("g-img", {"class": "uW5pk"}) # Condition is taken from image icon
    image = condIcon.find("img")
    condition = image.get('alt') # This icon is overall weather for the day, and is alt attribute

    div3 = soup.find("div", {"class": "gNCp2e"})
    high = div3.find("span", {"class": "wob_t"}).text
    div4 = soup.find("div", {"class": "QrNVmd ZXCv8e"})
    low = div4.find("span", {"class": "wob_t"}).text

    div5 = soup.find("div", {"class": "wtsRwe"})
    humid = div5.find("span", {"id": "wob_hm"}).text

    sp = loc.split(",") # Modify names to appropriate format for db
    loc = sp[0]
    low = low + " " + units
    high = high + " " + units
    print(loc, "weather on", d, ":", low, high, humid, condition)
    pushData(loc, d, low, high, humid, condition)

def checkIfHasWords(str): # If at least 1 character is a letter, it is accepted
    for i in str:
        if i.isalpha():
            return True
    return False

InputFile = open(city_input_directory, 'r') # read only, be sure to change directory for your own directory
CityList = InputFile.readlines()
for city in CityList:
    if checkIfHasWords(city)==False:
        break
    print(city)
    CollectCityWx(city) # collects, then sends
conn.close()
