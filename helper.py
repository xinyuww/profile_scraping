from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from parameters import par
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import logging


def search_subject(subject, driver):
	driver.get('https:www.google.com')
	sleep(3)

	search_query = driver.find_element_by_name('q')
	search_query.send_keys('site:linkedin.com/in/ {} Columbia Business School'.format(subject))
	sleep(1)
	search_query.send_keys(Keys.RETURN)
	sleep(3)

	linkedin_urls = driver.find_elements_by_class_name('iUh30')
	linkedin_urls = [url.text for url in linkedin_urls]
	sleep(2)

	print("Done searching subject")

	'''
	Select the correct LinkedIn url
	'''
	correct_urls = []

	for i in range(len(linkedin_urls)):
		driver.get(linkedin_urls[i])
		sleep(5)
		soup = BeautifulSoup(driver.page_source, 'lxml')
		name = soup.find('h1', class_='pv-top-card-section__name').text.replace('\n', '').replace('    ', '').replace('  ', '')
		schools = soup.find_all('h3', class_='pv-entity__school-name t-16 t-black t-bold')
		
		for j in range(len(schools)):
			print(schools[j].text)
			if schools[j].text == 'Columbia Business School':
				'''
				Need to check degree as well
				'''
				check_name = 0
				for part in name.split(' '):
					print(part)
					print(subject.split(' '))
					check_name
					if part in subject.split(' '):
						check_name = 1
					print(check_name)
				if check_name:
					correct_urls.append(linkedin_urls[i])
	# for i in range(len(correct_urls)):
	# 	if '?locale=de_DE' in correct_urls[i] and correct_urls[i].replace('?locale=de_DE', '') in correct_urls:
	# 		correct_urls.remove(correct_urls[i])
	notes = ''

	if not correct_urls:
		print("No results found")
		url = 'no results'
		soup = None
		logging.debug('No LinkedIn results found')
	else:
		if len(correct_urls)-1:
			print("Multiple results found")
			notes = 'multiple results'
			logging.debug('Multiple possible results')
		url = correct_urls[0]
		driver.get(url)
		sleep(10)

		soup = BeautifulSoup(driver.page_source, 'lxml')

	return url, soup, notes


def text_finder(string, key='\n'):
	ind = [pos for pos, char in enumerate(string) if char == key]
	start = ind[-2]+1
	end = ind[-1]
	return string[start:end]


def exist(soup):
	return soup != None
