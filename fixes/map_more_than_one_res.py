import urllib.parse
import pandas as pd
import requests

df = pd.read_excel('inconsistenreleasedate.xlsx')

titles = df['report_title'].to_list()

headers = {
	"accept": "application/json",
	"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MWRlNTkwNTUwMTYyZmM3ZTEyYmMxNmMxMmRlNmU2OSIsInN1YiI6IjY2NDY2YTU1MWQ1Yzc2YmRhZTgyZTA3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vWvWAOCDMVVDjGXNWqdnJ0rNTI-LbwEJmtubjOBKdDk"
}

columns = [
	'tmdb_id',
	'report_title'
]
movies = pd.DataFrame(columns = columns)

for title in titles:
	parsed_query_filter = urllib.parse.quote(title)

	search_list_url = f"https://api.themoviedb.org/3/search/movie?query={parsed_query_filter}&include_adult=false&language=en-US&page=1"
	search_list = requests.get(search_list_url, headers=headers)
	search_status = search_list.status_code
	while search_status != 200:
		search_list = requests.get(search_list_url, headers=headers)
		search_status = search_list.status_code
	search_list = search_list.json()

	if len(search_list['results']) > 1:
		movie_id = movie_id = search_list['results'][0]['id']
		movies.loc[len(movies)] = {'tmdb_id': movie_id, 'report_title': title}
	
	print(title)

movies.to_excel('more_than_one_res.xlsx')
