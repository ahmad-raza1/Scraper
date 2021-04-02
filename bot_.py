import sys
import time
import constants
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
		chrome_options.add_argument('--headless')
		driver = webdriver.Chrome(options=chrome_options)
		driver.maximize_window()

		driver.get('https://www.semanticscholar.org/')
		search_bar = driver.find_element_by_xpath('//*[@id="search-form"]/div/div/input')
		search_bar.send_keys(query_str)
		search_bar.submit()

		while True:
			try:
				main_div = driver.find_element(By.CLASS_NAME, 'result-page')
				break
			except Exception as e:
				print("DOM loading...\n")

		splits = main_div.find_elements_by_css_selector('.cl-paper-row.serp-papers__paper-row.paper-row-normal')

		abst_getable = []
		abstract_expand_btns = []

		for x in range(len(splits)): 
		    try:
		        abstract_div = splits[x].find_element_by_css_selector('div.tldr-abstract-replacement')
		        abstract_expand_btns.append(abstract_div.find_element_by_css_selector('span.more.mod-clickable'))
		        abst_getable.append(True)

		    except:
		        abst_getable.append(False)

		print(abst_getable)

		for x in range(len(abstract_expand_btns)):
		    WebDriverWait(driver, constants.TIMEOUT).until(EC.visibility_of(abstract_expand_btns[x]))
		    driver.execute_script("arguments[0].click();", abstract_expand_btns[x])

		url_hrefs = main_div.find_elements_by_css_selector('div.cl-paper-row.serp-papers__paper-row > a')
		title_spans =  main_div.find_elements_by_css_selector('div > a > div > span')

		urls = [a.get_attribute('href') for a in url_hrefs]
		titles = [title.text.encode('utf8') for title in title_spans]

		abstract_spans = main_div.find_elements_by_css_selector('div.tldr-abstract-replacement.text-truncator')
		abstracts = [abstract.text.encode('utf8') for abstract in abstract_spans]

		list_ = []
		i = 0

		for x in range(len(splits)):
		    if abst_getable[x] == True:
		            list_.append(
		            {
		            "url" : urls[x],
		            "title" : titles[x],
		            "abstract" : abstracts[i]
		            }
		        );
		            i = i + 1
		    else:
		        list_.append(
		            {
		            "url" : urls[x],
		            "title" : titles[x],
		            "abstract" : ""
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
