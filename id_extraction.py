import urllib.parse
import pandas as pd
import requests
import psycopg2

conn = psycopg2.connect(
  database='movies',
  host='localhost',
  user='user',
  password='p@ss',
  port='5432'
)

cursor = conn.cursor()

df = pd.read_excel('netflixfiltered.xlsx')

titles = df['Title'].to_list()

headers = {
	"accept": "application/json",
	"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MWRlNTkwNTUwMTYyZmM3ZTEyYmMxNmMxMmRlNmU2OSIsInN1YiI6IjY2NDY2YTU1MWQ1Yzc2YmRhZTgyZTA3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vWvWAOCDMVVDjGXNWqdnJ0rNTI-LbwEJmtubjOBKdDk"
}

for title in titles:
	parsed_query_filter = urllib.parse.quote(title)

	search_list_url = f"https://api.themoviedb.org/3/search/movie?query={parsed_query_filter}&include_adult=false&language=en-US&page=1"
	search_list = requests.get(search_list_url, headers=headers)
	search_status = search_list.status_code
	while search_status != 200:
		search_list = requests.get(search_list_url, headers=headers)
		search_status = search_list.status_code
	search_list = search_list.json()

	if len(search_list['results']) == 0:
		continue

	movie_id = search_list['results'][0]['id']
	title = title.replace("'", "''")

	query = f"INSERT INTO tmdb_movie (tmdb_id, report_title) VALUES ({movie_id}, '{str(title)}')"

	try:
		cursor.execute(query)
		conn.commit()

		print('Inserted ' + title + '!!!')
	except Exception as e:
		conn.rollback()

		print('Could not insert movie ' + title + ' with id ' + str(movie_id) + ': ' + str(e))
		continue

print('FINISHED!!!')

	
