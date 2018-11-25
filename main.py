import research

def main():
	tobacco_research = research.Research('tobacco')
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

	final_df_sub = final_df[['id','title_display','author_display','journal','bibjson.link','score','keyword','publisher','subject','article_statistics.statistics']]
	final_df_sub = final_df_sub.rename(columns={'article_statistics.statistics':'article_statistics', 'bibjson.link':'full_text_link'})

	print('Save final full dataset on tobacco research as tobacco_research_full.csv for furture analytics')
	final_df.to_csv('tobacco_research_full.csv', index=False)
	print('Save final subset on tobacco research as tobacco_research_subset.csv for sample analysis')
	final_df_sub.to_csv('tobacco_research_subset.csv', index=False)


if __name__ == '__main__':
	print('************* Start main program **************')
	main()
	print('************* Finish main program. Saves all files **************')