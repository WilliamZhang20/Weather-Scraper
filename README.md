# Weather-Scraper

This is a web scraper I made for extracting weather data from Google.
The project is written in python, using the Beautiful Soup package and Requests library.

## Contents

The file main.py is a basic web scraper that takes input for a city and temperature unit (degrees Celsius or Fahrenheit), then prints out the temperature and weather condition.
The files wxDataBase.py and cityInput.txt are an expanded version that incorporates the use of the MySQL database. The Python file reads city names from the .txt file, with 1 city per line. Then, it scrapes weather data for each city (the daily minimum, daily maximum, humidity, and condition). Next, the data is pushed to a table in the database. If a table for that city does not exist, a new one is created and the data is pushed.  

## Getting Started

1) Install the libraries required for scraping data from the web.
	sudo pip install bs4 requests

2) If you want to push the weather data to a database, install libraries for MySQL. Since I ran everything on the Raspberry Pi Linux terminal, I used the [MariaDB server](https://en.wikipedia.org/wiki/MariaDB).  
	sudo apt update
	sudo apt upgrade
	sudo apt install mariadb-server
	sudo pip install mysql-connector-python	
	sudo mysql_secure_installation

3) Follow the installation prompts and access the MySQL server with:
	sudo mysql -u root -p

4) Next, create a database for storing the weather data for different cities:
	CREATE DATABASE weatherdb; 

5) Finally, clone the project:
	git clone https://github.com/WilliamZhang20/Weather-Scraper.git

## Usage    

One can schedule the program to run at a certain time period. 
By typing `crontab -e` into the terminal and `0 12 * * * file directory in your machine` into the crontab file that opens, the code will be executed every day at 12 pm, provided that the machine is on. 
