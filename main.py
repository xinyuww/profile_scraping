from profile import Profile
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from parameters import par
from time import sleep
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import pandas as pd
import logging


logging.basicConfig(filename='scraper.log', filemode='w',level=logging.DEBUG)
logging.warning('Start running')


'''
login LinkedIn
'''
driver = webdriver.Chrome(par['chromedriver'])
driver.get('https://www.linkedin.com')
sleep(10)

username = driver.find_element_by_class_name('login-email')
username.send_keys(par['login'])
sleep(1)

password = driver.find_element_by_class_name('login-password')
password.send_keys(par['password'])
sleep(1)

log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()
# time to react if there's a robot check
sleep(par['login_sleep'])

logging.info('Success: logged in LinkedIn')


# driver.get('https:www.google.com')
# sleep(2)

# search_query = driver.find_element_by_name('q')
# search_query.send_keys('site:linkedin.com/in/ Xinyu Wei linkedin')
# sleep(0.5)
# search_query.send_keys(Keys.RETURN)
# sleep(5)



'''
Scraping subjects' LinkedIn
'''
for i in range(par['start_num'], par['end_num']):
#for i in l:

	'''
	Load Excel
	'''
	print(i)

	df = pd.read_excel(par['input_dir'])
	ex_data = df.copy(deep=True)

	logging.info('Success: loaded excel')

	'''
	Write to excel
	'''
	if ex_data.loc[i]['LinkedIn URL'] == 'no results':
		subject = ''
		orig_name = ex_data.loc[i]['Full_Name'].split(' ')
		subject = orig_name[0] + ' ' + orig_name[-1]

		#subject = ex_data.loc[i]['Full_Name']
		logging.info('Start scraping for {}'.format(subject))


		#url = ex_data.loc[i]['LinkedIn URL']


		profile = Profile(subject, driver)

		ex_data.loc[i, 'LinkedIn URL'] = profile.url
		if profile.soup != None:
			print(profile.schools)
			print(profile.degrees)
			print(profile.fields)
			print(profile.school_dates)
			print(profile.titles)
			print(profile.companies)
			print(profile.company_dates)
			print(profile.durations)
			print(profile.locations)
			print(profile.languages)
			print(profile.proficiencies)

			logging.info('Success: LinkedIn results found')
			logging.info('Start: Writing to dataframe')
			ex_data.loc[i, 'Name'] = profile.linkedin_name
			for j in range(len(profile.schools)):
				ex_data.loc[i,'school.{}'.format(j+1)] = profile.schools[j]
				ex_data.loc[i,'degree.{}'.format(j+1)] = profile.degrees[j]
				ex_data.loc[i,'field.{}'.format(j+1)] = profile.fields[j]
				ex_data.loc[i,'date.{}'.format(j+1)] = profile.school_dates[j]
			for j in range(len(profile.companies)):
				ex_data.loc[i,'title.{}'.format(j+1)] = profile.titles[j]
				ex_data.loc[i,'company.{}'.format(j+1)] = profile.companies[j]
				ex_data.loc[i,'date.{}.1'.format(j+1)] = profile.company_dates[j]
				ex_data.loc[i,'duration.{}'.format(j+1)] = profile.durations[j]
				ex_data.loc[i,'location.{}'.format(j+1)] = profile.locations[j]
			for j in range(len(profile.languages)):
				ex_data.loc[i,'language.{}'.format(j+1)] = profile.languages[j]
				ex_data.loc[i,'proficiency.{}'.format(j+1)] = profile.proficiencies[j]
			ex_data.loc[i, 'Notes'] = profile.notes
			
		logging.info('Start: output to excel')
		ex_data.to_excel(par['output_dir'])

		logging.info('Finished scraping for {}'.format(subject))
	else:
		pass

logging.info('Start: quit driver')
driver.quit()

logging.warning('End')



