import requests
import time
from bs4 import BeautifulSoup

records = ['tt15255288']

for row in records:
	movie_details_url = f"http://imdb.com/title/{row}/?ref_=fn_tt_tt_1"
	movie_details = requests.get(movie_details_url, headers={'User-Agent': 'Chrome'})
	details_status = movie_details.status_code
	while details_status != 200:
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
	
	print('title: ' + title)
	print('rating: ' + str(rating))
	print('budget: ' + str(budget))
	print('openingWeekendUSnCanada: ' + str(openingWeekendUSnCanada))
	print('grossUSnCanada: ' + str(grossUSnCanada))
	print('grossWorldwide: ' + str(grossWorldwide))
	

