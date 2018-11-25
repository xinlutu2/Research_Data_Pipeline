"""Extract Weather data through: https://openweathermap.org/current for W.C. Morse 
   Transform json to .csv, and save on local filesystem 
"""

import logging
import os
import json
from pandas.io.json import json_normalize
import requests
import datetime

# enabloe logging messages to airflow
log = logging.getLogger(__name__)
api_key = '53e2067c8105f4cf7c07ccb68727965a'
# store staging directory in current working directory
local_dir = os.getcwd()

class Extract_Transform:
	@classmethod
	def get_weather(cls, **context):
		""" ├── <Store Name>
			│   ├── <pipeline_execution_date>_weather.csv
			│   ├── <pipeline_execution_date>_weather.csv
	
			.....

			Save weather.csv according to degsined file structure
			:type context: dict
			:rtype: list
		"""
		log.info('Start getting weather data')

		# getting execution date
		execution_date = context['ds']
		storage_name = context['params']['base']
		base = os.path.join(local_dir, storage_name)

		# base_url variable to store url 
		base_url = "http://api.openweathermap.org/data/2.5/weather?"
		coordinates = 'lat=37.831106&lon=-122.254110'
		complete_url = base_url + "appid=" + api_key + "&" + coordinates
		  
		response = requests.get(complete_url) 
		weather = response.json() 

		# F = 1.8(K - 273) + 32, convert Kelvin To Fahrenheit
		weather_df = json_normalize(weather['main'])
		weather_df['temp'] = 1.8*(weather_df['temp']-273)+32
		weather_df['temp_max'] = 1.8*(weather_df['temp_max']-273)+32
		weather_df['temp_min'] = 1.8*(weather_df['temp_min']-273)+32
		weather_df['date'] = execution_date
		weather_df['store_name'] = storage_name

		if not os.path.exists(base):
				os.makedirs(base)
		# save pandas dataframe as <Store Name>/<pipeline_execution_date>_weather.csv
		file_name = str(execution_date)+'_weather.csv'
		weather_df.to_csv(os.path.join(base,file_name))

		log.info('Finish getting weather data')



	




