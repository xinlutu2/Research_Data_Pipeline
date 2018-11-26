"""Python Operator to extract research information on <keyword> and save as .csv in local filesystem

"""

import logging
import os
import urllib.request
from urllib.error import URLError, HTTPError
import json
from pandas.io.json import json_normalize 
import pandas as pd

# enabloe logging messages to airflow
log = logging.getLogger(__name__)
# store staging directory in current working directory
local_dir = os.getcwd()


def flatten_json(json):
	"""Universal function to flatten 1-level nested json 
	"""
	return json_normalize(json)

def join_df(df_list, function):
	"""Universal function to join df with same column names
	  
	   :type df_list: list
	   :function: function to extract data from API 
	   (PLOS Search API: articles info, DOAJ API: journal info, article link) 
	   :rtype: pandas dataframe
	"""
	count = 0
	for df in df_list:
		# create the first df
		if count == 0:
			res_df = function(df)
			count += 1
		else:
			temp = function(df)
			res_df = res_df.append(temp, ignore_index=True, sort=False)
	return res_df

class Extract_Transform:
	@classmethod
	def save_csv(cls, **context):
		""" ├── <keyword>
			│   ├── <pipeline_execution_date>_research.csv
				├── <pipeline_execution_date>_research.csv
			.....

			Save research.csv according to degsined file structurex

			:type context: dict
			:rtype: list
		"""

		# getting execution date
		execution_date = context['ds']
		# getting base folder name: <keyword>
		keyword = context['params']['keyword']
		base = os.path.join(local_dir, keyword)

		tobacco_research = Research(keyword)
		articles = tobacco_research.PLOS_get_articles() # getting articles data

		# process journal_list, article_list for DOAJ API
		journal_list = set(articles['journal'])
		article_list = set(articles['id'])
		# drop nan
		journal_list = set(filter(lambda x: x == x , journal_list))
		article_list = set(filter(lambda x: x == x , article_list))

		journals = join_df(journal_list, tobacco_research.DOAJ_journals) # journal data
		article_text_link = join_df(article_list, tobacco_research.DOAJ_articles) # journal article link

		# join article data with journal article link on doi_id
		final_df = articles.merge(article_text_link, how='inner', left_on='id', right_on='id')
		# join article data with journal data
		final_df = final_df.merge(journals, how='inner', left_on='journal', right_on='title')

		
		# create file strcture
		if not os.path.exists(base):
			os.makedirs(base)

		file_name = str(execution_date)+'_research.csv'
		final_df.to_csv(os.path.join(base,file_name)) # save final .csv
		log.info('Finish saving files to local')


class Research:
	def __init__(self, keyword):
		self.keyword = keyword # store keyword for research info: 'tobacco'
		self.key = 't5XVxCxsjzVoZnUWMGgJ' # PLOS API key

	def PLOS_get_articles(self): 
		"""Collects article data from the PLOS Search API (http://api.plos.org/solr/examples/)
	  
		   :type keyword: str
		   :type api: str
		   :rtype: pandas dataframe
		"""
		base_url = 'http://api.plos.org/search?q=title:'
		api_url = '&wt=json&api_key=' + self.key
		complete_url = base_url + self.keyword+ api_url
		
		connection = urllib.request.urlopen(complete_url)
		response = json.load(connection)
		
		# get total records 
		total_records_num = response['response']['numFound']
		log.info(total_records_num, 'records found.')
		log.info('Starting fetching all journal article records')
		
		start_end_url = '&start=1&rows=' + str(total_records_num)
		complete_url = base_url + self.keyword + start_end_url + api_url
		
		connection = urllib.request.urlopen(complete_url)
		response = json.load(connection)
		
		result = response['response']['docs']
		result_df = flatten_json(result)
		
		# data processing
		result_df['journal'] = result_df['journal'].str.replace('PLOS','PLoS')
		result_df = result_df[['id','eissn','title_display','article_type','author_display','journal','publication_date','score','abstract']]
		result_df['keyword'] = self.keyword
		log.info('Finishing fetching all journal article records')
		return result_df

	def DOAJ_articles(self, article_id):
		"""Collects journal article online links from the DOAJ API (https://doaj.org/api/v1/docs#!/Search/get_api_v1_search_articles_search_query)
	  
		   :type article_id: str
		   :rtype: pandas dataframe
		"""
		base_url = 'https://doaj.org/api/v1/search/articles/'
		journal_url = 'doi:'+ article_id # exact based on unique doi_id 
		page_url = '?page=1&pageSize=10'
		complete_url = base_url + journal_url + page_url
		
		try:
			connection = urllib.request.urlopen(complete_url)
		except HTTPError as e:
			print('Error code: ', e.code)
			return
		except URLError as e:
			print('Reason: ', e.reason)
			return

		log.info('Starting fetching all article link records')
		log.info('******* Articles links might take serveral minutes *******')
		log.info(complete_url)

		response = json.load(connection)

		# handle articles without full_text access
		if len(response['results']) == 0:
			log.info(article_id + ' not found')
			return
		result_df = flatten_json(response['results']) 
		result_df = result_df[['bibjson.link']]
		result_df['bibjson.link'] = result_df['bibjson.link'][0][0]['url'] # extract url
		result_df['id'] = article_id
		log.info('Finishing fetching all article link records')
		return result_df

	def DOAJ_journals(self, journal_title):
		"""Collects journal data from the DOAJ API (https://doaj.org/api/v1/docs#!/Search/get_api_v1_search_articles_search_query)
	  
		   :type journal_title: str
		   :rtype: pandas dataframe
		"""
		base_url = 'https://doaj.org/api/v1/search/journals/'
		journal_url = 'title:'+ journal_title # bibjson.journal.title.exact not working
		page_url = '?page=1&pageSize=10'
		complete_url = base_url + journal_url + page_url
		
		try:
			connection = urllib.request.urlopen(complete_url)
		except HTTPError as e:
			log.info('Error code: ', e.code)
			return
		except URLError as e:
			log.info('Reason: ', e.reason)
			return

		log.info('Starting fetching all journal records')
		log.info(complete_url)
		connection = urllib.request.urlopen(complete_url)
		response = json.load(connection)
		result = [res['bibjson'] for res in response['results'] if res['bibjson']['title'] == journal_title] # mutiple results returned
		
		if len(result) == 0:
			log.info(journal_title + ' not found in DOAJ')
			return
			
		result_df = flatten_json(result) 
		# select key columns
		result_df = result_df[['title','provider','publisher','subject','active','article_statistics.statistics','author_copyright.copyright','author_publishing_rights.publishing_rights','editorial_review.process','format','language','plagiarism_detection.detection']]
		result_df['subject'] = result_df['subject'][0][0]['term'] # process subject column
		log.info('Finishing fetching all journal records')
		return result_df


	