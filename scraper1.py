from flask import Flask, render_template, request, flash
import time
from datetime import datetime
import base64
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import mysql.connector

mydb = mysql.connector.connect(host="h1.host.filess.io", user="dudenv2_bystreamwe", passwd="239848e4ad651c7b21981c6cd1fea4bf6ec5c444", database="dudenv2_bystreamwe", port="3307")
mycursor = mydb.cursor()

def add_data(wort, gebrauch):
	try:
		sql = "INSERT INTO wort_erg (wort, gebrauch) VALUES (%s, %s)"
		val = (wort, gebrauch)
		mycursor.execute(sql, val)
		mydb.commit()
	except:
                print("Error")

def add_data_other(wort, gebrauch):
	try:
		sql = "INSERT INTO other (wort, gebrauch) VALUES (%s, %s)"
		val = (wort, gebrauch)
		mycursor.execute(sql, val)
		mydb.commit()
	except:
                print("Error")



# Chrome Options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument ("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")



# Starting Web Driver
##driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
driver = webdriver.Chrome(r"./chromedriver.exe")
driver.get("http://www.google.com/")


count = 0
liste = ['test']

with open('deutsch.txt') as fp:
    contents = fp.readlines()


def scrape():
	for entry in contents:
		try:
			driver.get(f"https://www.duden.de/rechtschreibung/{entry}")
			gebrauch = driver.find_element(By.CSS_SELECTOR, "body > div.dialog-off-canvas-main-canvas > div.tabloid > div.tabloid__sheet.tabloid__sheet--has-sidebar.tabloid__sheet--has-insert.tabloid__sheet--has-main.tabloid__sheet--has-main-top > main > article > dl:nth-child(5) > dd")
			result = gebrauch.get_attribute("innerHTML")
			liste.append(entry)
			if result == 'bildungssprachlich':
				add_data(entry, 'bildungssprachlich')
			if result == 'gehoben':
				add_data(entry, 'gehoben')
			if result != 'bildungssprachlich':
				if result != 'gehoben':
					add_data_other(entry, result)

		except:
                        print(f"{entry} Not Found")
		
	
scrape()
