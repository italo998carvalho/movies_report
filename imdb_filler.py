import requests
import psycopg2
import time
from bs4 import BeautifulSoup

conn = psycopg2.connect(
  database='movies',
  host='localhost',
  user='user',
  password='p@ss',
  port='5432'
)

cursor = conn.cursor()

query = "SELECT imdb_id FROM imdb_movie WHERE imdb_title IS NULL;"

cursor.execute(query)
records = cursor.fetchall()

for row in records:
	imdb_id = row[0]

	movie_details_url = f"http://imdb.com/title/{imdb_id}/?ref_=fn_tt_tt_1"
	print('------1')
	movie_details = requests.get(movie_details_url, headers={'User-Agent': 'Chrome'})
	print('------2')
	details_status = movie_details.status_code
	while details_status != 200:
		print('---')
		print(imdb_id)
		print(details_status)
		time.sleep(50/1000)
		movie_details = requests.get(movie_details_url, headers={'User-Agent': 'Chrome'})
		details_status = movie_details.status_code

	soup = BeautifulSoup(movie_details.content, "html.parser")

	title = soup.title.text

	rating = soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'}).text
	rating = float(rating.split('/')[0])

	budget, openingWeekendUSnCanada, grossUSnCanada, grossWorldwide = None, None, None, None
	try:
		box_office = soup.find('div', {'data-testid': 'title-boxoffice-section'}).find('ul')
	except:
		pass
	
	try:
		budget = box_office.find('li', {'data-testid': 'title-boxoffice-budget'}).find('li', {'role': 'presentation'}).text
	except:
		pass

	try:
		openingWeekendUSnCanada = box_office.find('li', {'data-testid': 'title-boxoffice-openingweekenddomestic'}).find('li', {'role': 'presentation'}).text
	except:
		pass

	try:
		grossUSnCanada = box_office.find('li', {'data-testid': 'title-boxoffice-grossdomestic'}).find('li', {'role': 'presentation'}).text
	except:
		pass

	try:
		grossWorldwide = box_office.find('li', {'data-testid': 'title-boxoffice-cumulativeworldwidegross'}).find('li', {'role': 'presentation'}).text
	except:
		pass
	
	if budget is not None:
		budget = "'" + budget + "'"
	else:
		budget = 'NULL'

	if openingWeekendUSnCanada is not None:
		openingWeekendUSnCanada = "'" + openingWeekendUSnCanada + "'"
	else:
		openingWeekendUSnCanada = 'NULL'
	
	if grossUSnCanada is not None:
		grossUSnCanada = "'" + grossUSnCanada + "'"
	else:
		grossUSnCanada = 'NULL'
	
	if grossWorldwide is not None:
		grossWorldwide = "'" + grossWorldwide + "'"
	else:
		grossWorldwide = 'NULL'
	
	title = title.replace("'", "''")
	
	query = f"""
		UPDATE
			imdb_movie
		SET
			imdb_title='{title}',
			rating='{rating}',
			budget={budget},
			openning_week_us_canada={openingWeekendUSnCanada},
			gross_worldwide={grossWorldwide},
			gross_us_canada={grossUSnCanada}
		WHERE
			imdb_id='{imdb_id}'
	"""
	try:
		cursor.execute(query)
		conn.commit()

		print('Inserted ' + title + '!!!')
	except Exception as e:
		conn.rollback()

		print('Could not insert movie ' + title + ' with id ' + str(imdb_id) + ': ' + str(e))
		continue

print('FINISHED!!!')
	

