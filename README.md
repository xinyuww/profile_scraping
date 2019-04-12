# profile_scraping
Web scraping for *** profiles (hidden words decodable from the code, the same applies to the ones below) 
\nThis code is still under development.

To run the code, you need to install/download the following:
1) BeautifulSoup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
2) Chromedriver (http://chromedriver.chromium.org/)
3) Selenium (https://selenium-python.readthedocs.io/installation.html)
  -  For Mac users, simply do 'pip install selenium' in terminal

Start by entering the following in the parameter.py:
1) *** login email and *** password
2) chromdriver location in your computer
3) input excel file location and output excel file location (can be the same as the input) 
4) subject number that you want to start & end with
5) sleep time after clicking login, allow 100s if your account needs to pass the robot check

**To scrape, run main.py**

Output:
1) An excel file with subjects' *** profile information
2) scraper.log 
  - log of inforamtion of the run
  - allows you to track the scraping process for a particular subject
