import requests
import psycopg2
import time

conn = psycopg2.connect(
  database='movies',
  host='localhost',
  user='user',
  password='p@ss',
  port='5432'
)

cursor = conn.cursor()

query = "SELECT tmdb_id FROM tmdb_movie;"

cursor.execute(query)
records = cursor.fetchall()

headers = {
	"accept": "application/json",
	"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MWRlNTkwNTUwMTYyZmM3ZTEyYmMxNmMxMmRlNmU2OSIsInN1YiI6IjY2NDY2YTU1MWQ1Yzc2YmRhZTgyZTA3MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vWvWAOCDMVVDjGXNWqdnJ0rNTI-LbwEJmtubjOBKdDk"
}

for row in records:
	movie_id = row[0]

	movie_details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
	movie_details = requests.get(movie_details_url, headers=headers)
	details_status = movie_details.status_code
	while details_status != 200:
		time.sleep(50/1000)
		movie_details = requests.get(movie_details_url, headers=headers)
		details_status = movie_details.status_code
	movie_details = movie_details.json()

	budget = movie_details['budget']
	tmdb_title = movie_details['title']
	revenue = movie_details['revenue']
	imdb_id = movie_details['imdb_id']

	movie_release_dates_url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates"
	movie_release_dates = requests.get(movie_release_dates_url, headers=headers)
	release_dates_status = movie_release_dates.status_code
	while release_dates_status != 200:
		time.sleep(50/1000)
		movie_release_dates = requests.get(movie_release_dates_url, headers=headers)
		release_dates_status = movie_release_dates.status_code
	movie_release_dates = movie_release_dates.json()

	theater_release_date = None
	streaming_release_date = None
	for result in movie_release_dates['results']:
		if result['iso_3166_1'] == 'US':
			for release in result['release_dates']:
				if release['type'] == 2 and theater_release_date is None:
					theater_release_date = release['release_date']

				if release['type'] == 3:
					theater_release_date = release['release_date']
				
				if release['type'] == 4 and release['note'] == 'Netflix':
					streaming_release_date = release['release_date']
	
	if streaming_release_date is None:
		streaming_release_date = 'NULL'
	else:
		streaming_release_date = "'" + streaming_release_date + "'"

	if theater_release_date is None:
		theater_release_date = 'NULL'
	else:
		theater_release_date = "'" + theater_release_date + "'"
	
	tmdb_title = tmdb_title.replace("'", "''")

	query = f"""
		UPDATE
			tmdb_movie
		SET
			tmdb_title='{tmdb_title}',
			budget='{budget}',
			release_date_streaming={streaming_release_date},
			release_date_theater={theater_release_date},
			revenue='{revenue}'
		WHERE
			tmdb_id={movie_id}
	"""
	try:
		cursor.execute(query)
		conn.commit()

		print('Inserted ' + tmdb_title + '!!!')
	except Exception as e:
		conn.rollback()

		print('Could not insert movie ' + tmdb_title + ' with id ' + str(movie_id) + ': ' + str(e))
		continue

	query = f"INSERT INTO imdb_movie (tmdb_id, imdb_id) VALUES ({movie_id}, '{imdb_id}');"
	try:
		cursor.execute(query)
		conn.commit()

		print('Inserted IMDB ' + str(imdb_id) + '!!!')
	except Exception as e:
		conn.rollback()

		print('Could not insert imdb movie ' + str(imdb_id) + ': ' + str(e))
		continue

	print('---------------------')

print('FINISHED!!!')
