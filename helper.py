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


# #driver.get('https://www.linkedin.com/in/joaquin-del-rosario-768961b7/')
# #driver.get('https://www.linkedin.com/in/xinyu-wei-a9126911a/')

# #driver.execute_script("window.scrollTo(0, 2080)")


# # soup = BeautifulSoup(driver.page_source, 'lxml')
# # print(soup.find_all('h3', text='Languages'))
# # driver.quit()
# # print(soup)
# # button_id = soup.find_all('h3', text='Languages')[0].find_parent('div').find('button')['id']

# # element = driver.find_element_by_id(button_id)
# # driver.execute_script("arguments[0].scrollIntoView();", element)
# # sleep(5)



# name = soup.find('h1').text

# '''
# Coding experience
# '''
# title_list = []
# company_list = []
# date_list = []
# duration_list = []
# location_list = []

# experience_node = soup.find_all('section', class_='experience-section')[0]
# experiences = experience_node.find_all('li', class_='pv-profile-section')

# num_experiences = len(experiences)
# #current_node = soup.find('li', class_='pv-profile-section')
# for i in range(num_experiences):

# 	current_node = experiences[i]

# 	title_list.append(current_node.find('h3').text)
# 	company_list.append(current_node.find('span', class_="pv-entity__secondary-title").text)
# 	duration_list.append(current_node.find('span', class_="pv-entity__bullet-item-v2").text)
	
# 	date_string = current_node.find('h4', class_="pv-entity__date-range").text
# 	date_list.append(text_finder(date_string, '\n'))

# 	location_string = current_node.find('h4', class_="pv-entity__location").text
# 	location_list.append(text_finder(location_string, '\n'))

# '''
# Coding education
# '''

# school_list = []
# degree_list = []
# field_list = []
# school_date_list = []

# education_node = soup.find_all('section', class_='education-section')[0]
# educations = education_node.find_all('li')

# num_educations = len(educations)

# for i in range(num_educations):
# 	current_node = educations[i]

# 	school_list.append(current_node.find('h3',class_="pv-entity__school-name").text)

# 	date_string = current_node.find('p',class_="pv-entity__dates").find_all('span')[-1].text
# 	print(date_string)
# 	school_date_list.append(text_finder(date_string, '\n'))

# 	degree_list.append(current_node.find_all('span',class_="pv-entity__comma-item")[0].text)

# 	if len(current_node.find_all('span',class_="pv-entity__comma-item")) > 1:
# 		field_list.append(current_node.find_all('span',class_="pv-entity__comma-item")[1].text)
# 	else:
# 		field_list.append('')

# '''
# Coding languages
# '''

# language_list = []
# proficiency_list = []

# if soup.find('section', class_='languages'):
# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1080);")
# 	sleep(5)
	
# 	expand_language_button = driver.find_element_by_xpath('//button[@aria-label="Expand languages section"]')
# 	expand_language_button.click()

# 	soup = BeautifulSoup(driver.page_source, 'lxml')



# 	languages = soup.find_all('ul', class_='pv-accomplishments-block__list')[0].find_all('li')

# 	for i in range(len(languages)):
# 		if exist(languages[i].find(class_='pv-accomplishment-entity__title')):
# 			language_list.append(text_finder(languages[i].find(class_='pv-accomplishment-entity__title').text))
# 		else:
# 			language_list.append('')
# 		if exist(languages[i].find(class_='pv-accomplishment-entity__proficiency')):
# 			proficiency_list.append(text_finder(languages[i].find(class_='pv-accomplishment-entity__proficiency').text))
# 		else:
# 			proficiency_list.append('')


# '''
# Saving to excel
# '''

# driver.quit()

# print(company_list)
# print(date_list)
# print(location_list)
# print(duration_list)
# print(school_list)
# print(school_date_list)
# print(field_list)
# print(degree_list)
# print(language_list)
# print(proficiency_list)
