import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

if __name__ == "__main__":

	argc = len(sys.argv)
	query = []

	if argc >= 2:
		for x in range(1, argc):
			query.append(sys.argv[x])

		query_str = " ".join(query) + ".pdf"
		
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		driver = webdriver.Chrome(options=chrome_options)

		driver.get('https://www.semanticscholar.org/')
		search_bar = driver.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
		search_bar.send_keys(query_str)
		search_bar.submit()

		driver.set_page_load_timeout(20)

		results = driver.find_elements_by_xpath('//*[@id="main-content"]/div[1]/div[2]')
		results_urls = [result.get_attribute('href') for result in results]

		print(*results, sep = "\n") 
		driver.close()

	else:
		print("Please enter the search query!")
		exit(1)
