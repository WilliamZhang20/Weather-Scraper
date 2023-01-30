import os
import MySQLdb
from dotenv import load_dotenv

# create the MySQL server username and password environment variables from .env
load_dotenv()

mysql_username = os.getenv('mysql_username')
mysql_password = os.getenv('mysql_password')

conn = MySQLdb.connect(
    host = 'localhost',
    user = mysql_username,
    password = mysql_password,
    database = 'weatherdb'
)

cursor = conn.cursor()
cursor2 = conn.cursor()

# Input processing: User enters dates for time span (e.g. January 1 - December 31)
# See README for more details on i/o process
query = input("Please enter two hyphen-separated dates to get a weather average.\n")
hyphen = query.find('-')

def processDate(time):
    time = time.split()
    time[1] = int(time[1])
    return time

start = processDate(query[0:(hyphen-1)])
finish = processDate(query[(hyphen+2):])

cursor.execute("SHOW TABLES")

def processTemp(temp):
    idx = temp.find("°") - 1
    return int(temp[0:idx])

def processHumid(humid):
    idx = humid.find("%")
    return int(humid[0:idx])

def adjust(number):
    return round(number, 1)

def processCondition(cond):
    cond = cond.lower() # puts all to lowercase
    res = [] # index of condition array to increment (counts # of days)
    idxRain = cond.find("rain")
    idxSnow = cond.find("snow")
    idxStorm = cond.find("storm")
    idxShowers = cond.find("showers")
    idxSunny = cond.find("sunny")
    idxCloudy = cond.find("cloud")
    idxMost = cond.find("most")
    idxPart = cond.find("part")
    if idxSunny != -1 or (idxCloudy != -1 and idxPart != -1):
        res = [0] # sunny or partly cloudy -> sunny
    elif idxCloudy != -1 or (idxMost != -1 and idxCloudy != -1):
        res = [1] # cloudy or mostly cloudy -> cloudy
    elif (idxRain != -1 or idxShowers !=-1 or idxStorm != -1) and idxSnow==-1:
        res = [2] # rain or showers or storm and no snow -> rainy
    elif idxSnow != -1:
        res = [3] # snowy
    elif idxRain != -1 and idxSnow != -1:
        res = [2, 3] # rainy and snowy
    else: res = [0]
    return res

def monthOrder(month):
    if month == "January":
        return 1
    elif month == "February":
        return 2
    elif month == "March":
        return 3
    elif month == "April":
        return 4
    elif month == "May":
        return 5
    elif month == "June":
        return 6
    elif month == "July":
        return 7
    elif month == "August":
        return 8
    elif month == "September":
        return 9
    elif month == "October":
        return 10
    elif month == "November":
        return 11
    elif month == "December":
        return 12
    return 0

def isInQuery(date):
    if monthOrder(start[0]) < monthOrder(date[0]) or monthOrder(finish[0]) > monthOrder(date[0]):
        return False
    elif monthOrder(start[0]) == monthOrder(date[0]) and date[1] < start[1]:
        return False
    elif monthOrder(finish[0]) == monthOrder(date[0]) and finish[1] < date[1]:
        return False
    return True

maxHigh = [" ", -100]
minHigh = [" ", 100]
maxLow = [" ", -100]
minLow = [" ", 100]
maxHumid = [" ", -1]
minHumid = [" ", 100]
maxSunny = [" ", -365]
maxCloudy = [" ", -365]
maxRainy = [" ", -365]
maxSnowy = [" ", -365]

for table in cursor:
    city = table[0]
    cursor2.execute("SELECT * FROM {};".format(city))
    res = cursor2.fetchall()
    totalRows = 0
    totalLow = 0
    totalHigh = 0
    totalHumid = 0
    wxConditions = [0, 0, 0, 0] # stores num. of sunny, cloudy, rainy, snowy days
    for row in res:
        date = processDate(row[0][0:(row[0].find(","))])
        if isInQuery(date)==False: # if date not in query, skip
            continue
        totalRows += 1
        totalLow += processTemp(row[1])
        totalHigh += processTemp(row[2])
        totalHumid += processHumid(row[3])
        conditionIdxs = processCondition(row[4])
        for num in conditionIdxs:
            wxConditions[num] += 1
    if totalRows < 7:
        # too few dates available for the selected query
        continue
    avgLow = adjust(totalLow / totalRows)
    avgHigh = adjust(totalHigh / totalRows)
    avgHumid = adjust(totalHumid / totalRows)
    sunny = adjust((wxConditions[0] / totalRows) * 100)
    cloudy = adjust((wxConditions[1] / totalRows) * 100)
    rainy = adjust((wxConditions[2] / totalRows) * 100)
    snowy = adjust((wxConditions[3] / totalRows) * 100)
    # checking for max/min low, high, humid
    if avgHigh > maxHigh[1]:
        maxHigh[0] = city
        maxHigh[1] = avgHigh
    elif avgHigh < minHigh[1]:
        minHigh[0] = city
        minHigh[1] = avgHigh
    if avgLow > maxLow[1]:
        maxLow[0] = city
        maxLow[1] = avgLow
    elif avgLow < minLow[1]:
        minLow[0] = city
        minLow[1] = avgLow
    if avgHumid > maxHumid[1]:
        maxHumid[0] = city
        maxHumid[1] = avgHumid
    elif avgHumid < minHumid[1]:
        minHumid[0] = city
        minHumid[1] = avgHumid
    if sunny > maxSunny[1]:
        maxSunny[0] = city
        maxSunny[1] = sunny
    if cloudy > maxCloudy[1]:
        maxCloudy[0] = city
        maxCloudy[1] = cloudy
    if rainy > maxRainy[1]:
        maxRainy[0] = city
        maxRainy[1] = rainy
    if snowy > maxSnowy[1]:
        maxSnowy[0] = city
        maxSnowy[1] = snowy
    print("{}\'s averages: ".format(city), end='')
    print("Low: ", avgLow, "°C ", "High: ", avgHigh, "°C ", "Humidity: ", avgHumid, "%")
    print("Sunny days:", wxConditions[0], "Cloudy days:", wxConditions[1], "Rainy days:", wxConditions[2], "Snowy days: ", wxConditions[3], "\n")

def printMaxAndMins(maxHigh, minHigh, maxLow, minLow, maxHumid, minHumid, maxSunny, maxCloudy, maxRainy, maxSnowy):
    # Printing min and max low, high, humid and cities with most sun, cloud, rain, or snow
    if(maxHigh[1]==-100):
        print("No cities within the database had sufficient data within your timeframe")
        return
    print("City with max avg high:", maxHigh[0], "at", maxHigh[1], "°C")
    print("City with min avg high:", minHigh[0], "at", minHigh[1], "°C")
    print("City with max avg low:", maxLow[0], "at", maxLow[1], "°C")
    print("City with min avg low:", minLow[0], "at", minLow[1], "°C")
    print("Most humid city:", maxHumid[0], "at avg", maxHumid[1], "%")
    print("Least humid city:", minHumid[0], "at avg", minHumid[1], "%")
    print("Sunniest city:", maxSunny[0], "at", maxSunny[1], "% of time")
    print("Cloudiest city:", maxCloudy[0], "at", maxCloudy[1],"% of time")
    print("Rainiest city:", maxRainy[0], "at", maxRainy[1],"% of time")
    if maxSnowy[1] != 0:
        print("Snowiest city:", maxSnowy[0], "at", maxSnowy[1],"% of time")
    else:
        print("No cities in data had any snowy days in the time period queried")

printMaxAndMins(maxHigh, minHigh, maxLow, minLow, maxHumid, minHumid, maxSunny, maxCloudy, maxRainy, maxSnowy)
