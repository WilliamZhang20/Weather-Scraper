# Weather-Scraper

This is a web scraper I made to collect weather data for various cities from Google. This can be used to analyze and compare weather data between cities.

The project is written in Python, using the Beautiful Soup package and Requests library.

It also includes features that allow for the entry of data into a MySQL database and the analysis/extraction of that data.

## Contents

The file main.py is a basic web scraper that takes input for a city and temperature unit (degrees Celsius or Fahrenheit), then prints out the current temperature and weather condition.

The files wxDataBase.py and cityInput.txt are an expanded version that incorporates the use of the MySQL database. The Python file reads city names from the text file, with 1 city per line. Then, it scrapes weather data for each city from the web (the daily minimum temperature, maximum temperature, humidity, and condition). Next, the data is pushed to the database, with each city getting its own table. If a table for that city does not exist, a new one is created and the data is pushed. Or, if there already is data in the table for today's date, then nothing will be done with the table. 

The file wxAnalyze.py is used to analyze the data. The user can query a time period and the program will display averages for each city and the cities with maximums and minimums.

## Getting Started

1) First, install the libraries for scraping data from the web

```
    sudo pip3 install bs4 requests lxml 
```

2) If you want to push the weather data to a database, install libraries for MySQL. Since I ran everything on the Raspberry Pi Linux terminal, I used the [MariaDB server](https://en.wikipedia.org/wiki/MariaDB).  

```
    sudo pip3 install python-dotenv
    sudo apt update
    sudo apt upgrade
    sudo reboot
    sudo apt install mariadb-server
    sudo python3 -m pip install mysqlclient
    sudo mysql_secure_installation
```

3) After you have answered 'No' to all the installation prompts and set your password, access the MySQL server with:

```   
    sudo mysql -u root -p
```

4) Next, create a database for storing the weather data for different cities:

```    
    CREATE DATABASE weatherdb; 
```

5) Retrieve the code by cloning the project:

```    
    git clone https://github.com/WilliamZhang20/Weather-Scraper.git
```

6) Finally, you will need to create a file called `.env` defining the environment variables `mysql_username` and `mysql_password`.

    For example:

```
    mysql_username=your_username
    mysql_username=your_password
```

## Usage    

If your MySQL user remains root (as it is by default), then the keyword 'sudo' is required before the 'python3 filename.py'

One can schedule the program to run at a certain time period. 
By typing `crontab -e` into the terminal and `0 12 * * * sudo python3 (your directory)/Weather-Scraper/wxDataBase.py` into the crontab file that opens, the code will be executed every day at 12 pm, provided that the machine is on. The crontab time is based on the 24 hour clock. 

### Analyzing data

The user query for it should include two dates separted by a hyphen, for which the user would like data averages between those dates for each city. It will also print cities with maximum and minimum temperatures, humdities, and weather conditions.
An example could be 'June 24 - September 24' for a summer average. If a city has less than 1 week of data within the queried time frame, its data will not be considered.
