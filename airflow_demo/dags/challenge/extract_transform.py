"""...

"""

import logging
import os
import research

# enabloe logging messages to airflow
log = logging.getLogger(__name__)
# store staging directory in current working directory
local_dir = os.getcwd()

class Extract_Transform:
	"""...

	"""
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
		tobacco_research = research.Research(keyword)
		articles = tobacco_research.PLOS_get_articles() # getting articles data

		# process journal_list, article_list for DOAJ API
		journal_list = set(articles['journal'])
		article_list = set(articles['id'])
		# drop nan
		journal_list = set(filter(lambda x: x == x , journal_list))
		article_list = set(filter(lambda x: x == x , article_list))

		journals = research.join_df(journal_list, tobacco_research.DOAJ_journals) # journal data
		article_text_link = research.join_df(article_list, tobacco_research.DOAJ_articles) # journal article link

		# join article data with journal article link on doi_id
		final_df = articles.merge(article_text_link, how='inner', left_on='id', right_on='id')
		# join article data with journal data
		final_df = final_df.merge(journals, how='inner', left_on='journal', right_on='title')

		# getting execution date
		execution_date = context['ds']
		# getting base folder name: <keyword>
		keyword = context['params']['keyword']
		base = os.path.join(local_dir, keyword)
		
		# create file strcture
		if not os.path.exists(base):
			os.makedirs(base)

		file_name = str(execution_date)+'_research.csv'
		final_df.to_csv(os.path.join(base,file_name)) # save final .csv

	