from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from parameters import par
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import logging
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains


def text_finder(string, key='\n'):
	ind = [pos for pos, char in enumerate(string) if char == key]
	start = ind[-2]+1
	end = ind[-1]
	return string[start:end]


def exist(soup):
	return soup != None


def check_hidden(soup):
	button_tag = soup.find_all('button', class_='pv-profile-section__see-more-inline')
	if len(button_tag) >= 1:
		logging.info('Exist expand background section')
		return True
	else:
		logging.info('Nothing to expand in background section')
		return False


def get_expanded_soup(soup, driver):
	button_tag = soup.find_all('button', class_='pv-profile-section__see-more-inline')
	for tag in button_tag:
		ID = tag.find_parent()['id']
		button = driver.find_element_by_xpath('//*[@id="{}"]/button'.format(ID))
		button.click()
		sleep(3)
	soup_new = BeautifulSoup(driver.page_source, 'lxml')
	return soup_new


def check_language(soup):
	return soup.find('section', class_='languages')


def get_languages_soup(soup, driver):
	ID = soup.find_all("h3", string="Languages")[0].find_parent().find_all('button')[0]['id']
	button = driver.find_element_by_xpath('//*[@id="{}"]'.format(ID))
	button.click()
	sleep(3)
	soup_new = BeautifulSoup(driver.page_source, 'lxml')
	return soup_new

def check_school(school):
	name = school.text.split(' ')
	if 'Columbia' in name and 'Business' in name:
		return True
	else:
		return False

def check_experience(company, title):
	if check_school(company) and 'MBA' in title:
		return True
	else:
		return False

def compute_score(linkedin_name, excel_name):
	score = 0
	for part in linkedin_name.split(' '):
		if part in excel_name.split(' '):
			score += 1
	return score

def get_label(text):
	deg_label = ['banchelor', 'mba', 'ms', 'msc', 'master', 'doctor', 'phd', 'ba', 'bba', 'bsc', 'be','bsba']
	for deg in deg_label:
		if deg in text.replace('.', '').lower().split(' '):
			return 'degree'
	return 'field'

def find_unique_url(linkedin_urls, ind):
	linkedin_urls = np.array(linkedin_urls)
	correct_urls = linkedin_urls[ind]
	unique_ID = []
	for url in correct_urls:
		start = url.index('/in/') + 4
		ID = url[start:]
		if '/' in ID:
			end = ID.index('/')
			ID = ID[:end]

		if ID not in unique_ID:
			unique_ID.append(ID)
	unique_url = ['www.linkedin.com/in/' + ID for ID in unique_ID]

	return unique_url

def search_subject(subject, driver):
	driver.get('https:www.google.com')
	sleep(3)

	search_query = driver.find_element_by_name('q')
	search_query.send_keys('site:linkedin.com/in/ {} linkedin Columbia Business School'.format(subject))
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
	scores = []

	for i in range(len(linkedin_urls)):

		driver.get(linkedin_urls[i])
		sleep(5)
		soup = BeautifulSoup(driver.page_source, 'lxml')
		name_node = soup.find('h1', class_='pv-top-card-section__name')
		if name_node:
			name_split = name_node.text.replace('\n', '').split(' ')
			while True:
			    try:
			        name_split.remove('')
			    except:
			        break
			name = ''
			for part in name_split:
				name = name + ' ' + part
			name = name[1:]

			schools = soup.find_all('h3', class_='pv-entity__school-name t-16 t-black t-bold')

			pass_school = 0

			for school in schools:
				if check_school(school):
					pass_school = 1
					break

			school_card = soup.find('span', class_='pv-top-card-v2-section__school-name')
			company_card = soup.find('span', class_='pv-top-card-v2-section__company-name')

			if company_card and 'Columbia Business School' in company_card:
				pass_school = 1

			if school_card and 'Columbia Business School' in school_card:
				pass_school = 1

			if pass_school:
				scores.append(compute_score(name, subject))


		else:
			pass

		

	# for i in range(len(correct_urls)):
	# 	if '?locale=de_DE' in correct_urls[i] and correct_urls[i].replace('?locale=de_DE', '') in correct_urls:
	# 		correct_urls.remove(correct_urls[i])
	notes = ''
	url = ''
	
	print("scores: ", scores)

	if sum(scores) == 0:
		print("No results found")
		url = 'no results'
		soup_new = None
		logging.debug('No LinkedIn results found')
	else:
		scores = np.array(scores)
		ind = np.where(scores == np.max(scores))[0]
		if len(ind) >1:

			urls = find_unique_url(linkedin_urls, ind)
			if len(urls) > 1:
				print('Multiple results found')
				notes = 'multiple results'
				logging.debug('Multiple possible results')
				for url in urls:
					logging.info(url)
			url = urls[0]

		elif len(ind) == 1:
			url = linkedin_urls[ind[0]]
	# if True:
	# 	notes = ''
	# 	url = 'https://www.linkedin.com/in/xinyu-wei-a9126911a/'
		
		print(url)

		driver.get(url)
		sleep(25)
		soup = BeautifulSoup(driver.page_source, 'lxml')

		if check_hidden(soup):
			soup_new = get_expanded_soup(soup, driver)
		else:
			soup_new = soup

	return url, soup_new, notes



