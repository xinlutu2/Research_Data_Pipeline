import research
import unittest

class TestResearch(unittest.TestCase):
	"""Unit test to test three main functions for Research class
	"""
	def test_plos_get_articles(self):
		test_research = research.Research('tobacco')
		test_articles = test_research.PLOS_get_articles() 
		test_columns = list(test_articles.columns.get_values())
		test_result = ['id','eissn','title_display','article_type','author_display','journal','publication_date','score','abstract','keyword']
		self.assertEqual(test_columns, test_result)

	def test_doaj_articles(self):
		test_research = research.Research('tobacco')
		test_article_link = test_research.DOAJ_articles('10.1371/journal.pone.0122610') 
		test_result = 'http://europepmc.org/articles/PMC4391913?pdf=render'
		self.assertEqual(test_article_link['bibjson.link'][0], test_result)

	def test_doaj_journals(self):
		test_research = research.Research('tobacco')
		test_journals = test_research.DOAJ_journals('PLoS Medicine') 
		test_result = 'PLoS Medicine'
		self.assertEqual(test_journals['title'][0], test_result)

if __name__ == '__main__':
	print('************* Start unittest **************')
	unittest.main()
	print('************* Finish unittest **************')