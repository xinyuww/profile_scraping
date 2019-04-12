from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from parameters import par
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import helper
from helper import text_finder, exist
import logging


class Profile:

	def __init__(self, subject, driver):
		self.name = subject
		self.driver = driver

		self.url, self.soup, self.notes = self.get_url(self.name, self.driver)
		if self.soup != None:
			self.linkedin_name = self.get_linkedin_name(self.soup)

			self.titles, self.companies, self.company_dates, self.durations, self.locations = self.get_companies(self.soup)
			self.schools, self.degrees, self.fields, self.school_dates = self.get_schools(self.soup)
			self.languages, self.proficiencies = self.get_languages(self.soup, self.driver)
		else:
			pass

	def get_url(self, subject, driver):
		return helper.search_subject(subject, driver)

	def get_linkedin_name(self, soup):
		return soup.find('h1').text.replace('\n', '').replace('    ', '').replace('  ', '')

	def get_companies(self, soup):
		title_list = []
		company_list = []
		date_list = []
		duration_list = []
		location_list = []

		experience_node = soup.find_all('section', class_='experience-section')

		if experience_node:
			experiences = experience_node[0].find_all('li', class_='pv-profile-section')
			num_experiences = len(experiences)

			for i in range(num_experiences):

				current_node = experiences[i]

				title_list.append(current_node.find('h3').text)
				company_list.append(current_node.find('span', class_="pv-entity__secondary-title").text)
				duration_list.append(current_node.find('span', class_="pv-entity__bullet-item-v2").text)
				
				date_string = current_node.find('h4', class_="pv-entity__date-range").text
				date_list.append(text_finder(date_string, '\n'))

				location_string = current_node.find('h4', class_="pv-entity__location").text
				location_list.append(text_finder(location_string, '\n'))
		else:
			logging.debug('No experience section found')

		return title_list, company_list, date_list, duration_list, location_list

	def get_schools(self, soup):
		school_list = []
		degree_list = []
		field_list = []
		school_date_list = []

		education_node = soup.find_all('section', class_='education-section')

		if education_node:
			educations = education_node[0].find_all('li')

			num_educations = len(educations)

			for i in range(num_educations):
				current_node = educations[i]

				school_list.append(current_node.find('h3',class_="pv-entity__school-name").text)

				date_string = current_node.find('p',class_="pv-entity__dates").find_all('span')[-1].text
				print(date_string)
				school_date_list.append(text_finder(date_string, '\n'))

				degree_list.append(current_node.find_all('span',class_="pv-entity__comma-item")[0].text)

				if len(current_node.find_all('span',class_="pv-entity__comma-item")) > 1:
					field_list.append(current_node.find_all('span',class_="pv-entity__comma-item")[1].text)
				else:
					field_list.append('')
		else:
			logging.debug('No education section found')

		return school_list, degree_list, field_list, school_date_list

	def get_languages(self, soup, driver):
		language_list = []
		proficiency_list = []

		if soup.find('section', class_='languages'):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1080);")
			sleep(5)

			try:
				expand_language_button = driver.find_element_by_xpath('//button[@aria-label="Expand languages section"]')
			except:
				logging.debug('Expand button not in view')
				return language_list, proficiency_list
			
			expand_language_button.click()

			soup_new = BeautifulSoup(driver.page_source, 'lxml')

			languages = soup_new.find_all('ul', class_='pv-accomplishments-block__list')[0].find_all('li')

			for i in range(len(languages)):
				if exist(languages[i].find(class_='pv-accomplishment-entity__title')):
					language_list.append(text_finder(languages[i].find(class_='pv-accomplishment-entity__title').text))
				else:
					language_list.append('')
				if exist(languages[i].find(class_='pv-accomplishment-entity__proficiency')):
					proficiency_list.append(text_finder(languages[i].find(class_='pv-accomplishment-entity__proficiency').text))
				else:
					proficiency_list.append('')
		else:
			logging.debug('No language section found')

		return language_list, proficiency_list
