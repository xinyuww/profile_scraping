from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from parameters import par
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from helper import *
import logging


class Profile:

	def __init__(self, subject, driver):
		self.name = subject
		self.driver = driver
		#self.input = url

		# self.url = 'https://www.linkedin.com/in/zachary-lyman-b4a1b044/'
		# self.driver.get(self.url)
		# self.soup = BeautifulSoup(driver.page_source, 'lxml')
		# self.notes = ''

		self.url, self.soup, self.notes = self.get_url(self.name, self.driver)
		if self.soup != None:
			self.linkedin_name = self.get_linkedin_name(self.soup)
			self.titles, self.companies, self.company_dates, self.durations, self.locations = self.get_companies(self.soup)
			self.schools, self.degrees, self.fields, self.school_dates = self.get_schools(self.soup)
			self.languages, self.proficiencies = self.get_languages(self.soup, self.driver)
		else:
			pass

	def get_url(self, subject, driver):
		return search_subject(subject, driver)

	def get_linkedin_name(self, soup):
		if soup.find('h1'):
			return remove_space(soup.find('h1').text, '\n')
		else:
			logging.debug('No name found')
			return None


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

				roles = current_node.find_all('li', class_='pv-entity__position-group-role-item')
				if roles:
					logging.info('Multiple roles for experience {}'.format(i))
					company_node = current_node.find('h3')
					company_list.append(text_finder(company_node.text))
					titles = []
					dates = []
					durations = []
					locations = []
					for role in roles:
						if role.find('h3'):
							titles.append(text_finder(role.find('h3').text))
						else: 
							titles.append('n/a')
						if role.find('h4', class_='pv-entity__location'):
							locations.append(text_finder(role.find('h4', class_='pv-entity__location').text))
						else:
							locations.append('n/a')
						if role.find('h4', class_='pv-entity__date-range'):
							dates.append(text_finder(role.find('h4', class_='pv-entity__date-range').text))
						else:
							dates.append('n/a')
						if role.find('span', class_='pv-entity__bullet-item-v2'):
							durations.append(role.find('span', class_='pv-entity__bullet-item-v2').text)
						else:
							durations.append('n/a')

					title_list.append(merge(titles))
					duration_list.append(merge(durations))
					date_list.append(merge(dates))
					location_list.append(merge(locations))
					
				else:

					# Find title
					title_node = current_node.find('h3')
					if title_node:
						title_list.append(title_node.text)
					else:
						title_list.append('')
						logging.debug('No title found for company {}'.format(i))

					# Find company
					company_node = current_node.find('span', class_="pv-entity__secondary-title")
					if company_node:
						company_list.append(company_node.text)
					else:
						company_list.append('')
						logging.debug('No company name found for company {}'.format(i))

					# Find duration
					duration_node = current_node.find('span', class_="pv-entity__bullet-item-v2")
					if duration_node:
						duration_list.append(duration_node.text)
					else:
						duration_list.append('')
						logging.debug('No duration found for company {}'.format(i))

					# Find date
					date_node = current_node.find('h4', class_="pv-entity__date-range")
					if date_node:
						date_string = date_node.text
						date_list.append(text_finder(date_string, '\n'))
					else:
						date_list.append('')
						logging.debug('No date found for company {}'.format(i))

					# Find location
					location_node = current_node.find('h4', class_="pv-entity__location")
					if location_node:
						location_string = location_node.text
						location_list.append(text_finder(location_string, '\n'))
					else:
						location_list.append('')
						logging.debug('No location found for company {}'.format(i))
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

				# Find school name
				school_node = current_node.find('h3',class_="pv-entity__school-name")
				if school_node:
					school_list.append(school_node.text)
				else:
					school_list.append('')
					logging.debug('No school name found for school {}'.format(i))

				# Find school date
				date_node = current_node.find('p',class_="pv-entity__dates")
				if date_node:
					date_string = date_node.find_all('span')[-1].text
					school_date_list.append(text_finder(date_string, '\n'))
				else:
					school_date_list.append('')
					logging.debug('No date found for school {}'.format(i))

				# Find degree info
				degree_node = current_node.find_all('span',class_="pv-entity__comma-item")
				if degree_node:
					if len(degree_node) > 1: 
						degree_list.append(degree_node[0].text)
						field_list.append(degree_node[1].text)
					elif len(degree_node) == 1:
						text = degree_node[0].text
						if get_label(text) == 'degree':
							degree_list.append(text)
							field_list.append('')
						elif get_label(text) == 'field':
							field_list.append(text)
							degree_list.append('')

				else:
					degree_list.append('')
					field_list.append('')
					logging.debug('No degree or field found for school {}'.format(i))
			
		else:
			logging.debug('No education section found')

		return school_list, degree_list, field_list, school_date_list


	def get_languages(self, soup, driver):
		language_list = []
		proficiency_list = []

		if check_language(soup):
			soup_new = get_languages_soup(soup, driver)

			try:
				languages = soup_new.find_all('ul', class_='pv-accomplishments-block__list')[0].find_all('li')

				for i in range(len(languages)):
					# Find language name
					language_node = languages[i].find(class_='pv-accomplishment-entity__title')
					if language_node:
						language_list.append(remove_space(text_finder(language_node.text), ''))
					else:
						language_list.append('')
						logging.debug('No language name found for language {}'.format(i))

					# Find proficiency
					proficiency_node = languages[i].find(class_='pv-accomplishment-entity__proficiency')
					if proficiency_node:
						proficiency_list.append(remove_space(text_finder(proficiency_node.text), ''))
					else:
						proficiency_list.append('')
						logging.debug('No proficiency found for language {}'.format(i))
			except:
				print("ERROR: Language index out of range")
				logging.debug("ERROR: Language index out of range")
		else:
			logging.debug('No language section found')

		return language_list, proficiency_list
