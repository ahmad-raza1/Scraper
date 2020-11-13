import sys
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == "__main__":

	argc = len(sys.argv)
	query = []

	if argc >= 2:
		for x in range(1, argc):
			query.append(sys.argv[x])

		query_str = " ".join(query)
		
		chrome_options = webdriver.ChromeOptions()
		#chrome_options.add_argument('--headless')
		driver = webdriver.Chrome(options=chrome_options)
		driver.maximize_window()

		driver.get('https://www.semanticscholar.org/')
		search_bar = driver.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
		search_bar.send_keys(query_str)
		search_bar.submit()

		time.sleep(10)

		main_div = driver.find_element(By.CLASS_NAME, 'result-page')
		
		a_tags = main_div.find_elements_by_css_selector('div.cl-paper-row.serp-papers__paper-row > a')
		title_spans = main_div.find_elements_by_css_selector('div > a > div > span')
		#abstract_expand = main_div.find_elements_by_css_selector('div.cl-paper-row.serp-papers__paper-row > div > div > span.more.mod-clickable')
		abstract_expand = main_div.find_elements(By.CLASS_NAME, 'more.mod-clickable')
		
		urls = [a.get_attribute('href') for a in a_tags]
		titles = [title.text for title in title_spans]
		
		time.sleep(20)
		
		timeout = 10
		for clickable in abstract_expand:
			WebDriverWait(driver, timeout).until(EC.visibility_of(clickable))
			clickable.click()
			time.sleep(10)
		
		#abstract_spans = main_div.find_elements_by_css_selector('div.cl-paper-abstract > span')
		abstract_spans = main_div.find_elements_by_css_selector('div.tldr-abstract-replacement.text-truncator')
		abstracts = [abstract.text for abstract in abstract_spans]

		list_ = []
		for url, title, abstract in zip(urls, titles, abstracts):
			list_.append(
				{
					"url" : url,
					"title" : title,
					"abstract" : abstract
				}
			);

		print(*list_, sep = "\n\n")

		with open('listfile.txt', 'w') as filehandle:
			for listitem in list_:
				filehandle.write('%s\n\n' % listitem)

		driver.close()

	else:
		print("Please enter the search query!")
		exit(1)
