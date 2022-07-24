# Sources:
# https://stackoverflow.com/questions/16780158/search-within-tags-with-beautifulsoup-python
# https://www.youtube.com/watch?v=cta1yCb3vA8
import requests
from bs4 import BeautifulSoup # NOTE: use sudo python3 when running. The module is for python3.

# In lin 10 below, I provided the user agent when making the HTTP request
# The server needs more information in requests to obtain JavaScript code
# To find user agent, simply Google search "my user agent"
hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

query = input("Which city's weather would you like? ")
URL = "https://www.google.com/search?q=%s+weather" % query
r = requests.get(URL, headers = hdrs)
soup = BeautifulSoup(r.content, 'lxml')

unitReq = input("Enter 1 for temperature in Celsius or 2 for Fahrenheit. ")
isCelsius = False

while unitReq != "1" and unitReq != "2":
        unitReq = input("1 for Celsius, 2 for Fahrenheit. Try again. ")
if unitReq=="1":
        isCelsius = True

loc = soup.find("div", {"id": "wob_loc"}).text
div1 = soup.find("div", {"class": "vk_bk wob-unit"})
if isCelsius==True:
        temp = soup.find("span", {"id": "wob_tm"}).text
        units = div1.find("span", {"aria-label": "°Celsius"}).text
else:
        temp = soup.find("span", {"id": "wob_ttm"}).text
        units = div1.find("span", {"aria-label": "°Fahrenheit"}).text
div2 = soup.find("div", {"class": "wob_dcp"})
condition = div2.find("span", {"id": "wob_dc"}).text
print(loc, "weather: ", temp, units, " ", condition)
