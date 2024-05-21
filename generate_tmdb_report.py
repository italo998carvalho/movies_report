import pandas as pd
import psycopg2

conn = psycopg2.connect(
  database='movies',
  host='localhost',
  user='user',
  password='p@ss',
  port='5432'
)

cursor = conn.cursor()

query = """
	SELECT
		*
	FROM
		tmdb_movie tmdb
	INNER JOIN
		imdb_movie imdb ON tmdb.tmdb_id = imdb.tmdb_id;
"""

cursor.execute(query)
records = cursor.fetchall()

columns = [
	'tmdb_id',
	'report_title',
	'tmdb_title',
	'tmdb_budget',
	'release_date_streaming',
	'release_date_theater',
	'revenue',
	'imdb_id',
	'imdb_title',
	'rating',
	'imdb_budget',
	'gross_worldwide',
	'gross_us_canada',
	'openning_week_us_canada'
]
movies = pd.DataFrame(columns = columns)

for row in records:
	tmdb_id = row[0]
	report_title = row[1]
	tmdb_title = row[2]
	tmdb_budget = row[3]
	release_date_streaming = row[4]
	release_date_theater = row[5]
	revenue = row[6]
	imdb_id = row[8]
	imdb_title = row[9]
	rating = row[10]
	imdb_budget = row[11]
	gross_worldwide = row[12]
	gross_us_canada = row[13]
	openning_week_us_canada = row[14]

	data = {
		'tmdb_id': tmdb_id,
		'report_title': report_title,
		'tmdb_title': tmdb_title,
		'tmdb_budget': tmdb_budget,
		'release_date_streaming': release_date_streaming,
		'release_date_theater': release_date_theater,
		'revenue': revenue,
		'imdb_id': imdb_id,
		'imdb_title': imdb_title,
		'rating': rating,
		'imdb_budget': imdb_budget,
		'gross_worldwide': gross_worldwide,
		'gross_us_canada': gross_us_canada,
		'openning_week_us_canada': openning_week_us_canada
	}

	movies.loc[len(movies)] = data

movies.to_excel('result_v2.xlsx')


