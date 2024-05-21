import pandas as pd
import numpy as np
import requests
import time

df = pd.read_excel('result_v2.xlsx')
df['release_streaming_date_country'] = np.nan
df_no_release_date = df[df['release_date_streaming'].isnull()]

ids = df_no_release_date['tmdb_id'].to_list()

headers = {
	"accept": "application/json",
	"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MWRlNTkwNTUwMTYyZmM3ZTEyYmMxNmMxMmRlNmU2OSIsInN1YiI6IjY2NDY2YTU1MWQ1Yzc2YmRhZTgyZTA3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vWvWAOCDMVVDjGXNWqdnJ0rNTI-LbwEJmtubjOBKdDk"
}

for id in ids:
	movie_release_dates_url = f"https://api.themoviedb.org/3/movie/{id}/release_dates"
	movie_release_dates = requests.get(movie_release_dates_url, headers=headers)
	release_dates_status = movie_release_dates.status_code
	while release_dates_status != 200:
		time.sleep(50/1000)
		movie_release_dates = requests.get(movie_release_dates_url, headers=headers)
		release_dates_status = movie_release_dates.status_code
	movie_release_dates = movie_release_dates.json()

	streaming_release_date = None
	country = None

	for result in movie_release_dates['results']:
		# If I find US, I'll try to fill the infos from US
		if result['iso_3166_1'] == 'US':
			for release in result['release_dates']:				
				if release['type'] == 4 and release['note'] == 'Netflix':
					streaming_release_date = release['release_date']
					country = 'US'
		
		# If I find Canada, and the country is not US, I'll try to fill the infos from Canada
		if result['iso_3166_1'] == 'CA' and country is not 'US':
			for release in result['release_dates']:				
				if release['type'] == 4 and release['note'] == 'Netflix':
					streaming_release_date = release['release_date']
					country = 'CA'
		
		# If not US nor Canada is set yet, I'll try to get the infos from the first place I find
		if streaming_release_date is None:
			for release in result['release_dates']:				
				if release['type'] == 4 and release['note'] == 'Netflix':
					streaming_release_date = release['release_date']
					country = result['iso_3166_1']
		
	if streaming_release_date is not None:
		row_index = df.loc[df['tmdb_id'] == int(id)].index[0]
		df.loc[row_index, 'release_date_streaming'] = streaming_release_date
		df.loc[row_index, 'release_streaming_date_country'] = country

		print(f"Release date from movie {id} set to {streaming_release_date} from {country}!!!")
	else:
		print(f"Couldn't find a release date for movie {id}!!!")

print('Finished!!!')

df.to_excel('result_v3.xlsx')
