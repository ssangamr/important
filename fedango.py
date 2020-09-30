import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage



def CrawlWords(url):
	resource = requests.get(url).text
	souped_resource = BeautifulSoup(resource,"html.parser")
	#print(souped_resource)
	title = souped_resource.find_all('title')

	
	for each_result in title:
		each_result_str = each_result.string
		final_title = each_result_str.split('|')
		global movie_name
		movie_name = str(final_title[0])
		print("Movie title Name:", movie_name)
		
	
	movie_locations = souped_resource.find('ul', attrs={'class':'mega-menu-cities-list'})	
	search_locations = movie_locations.find_all('a')
	#print(search_locations )
	AllLocations = []
	
	for each_location in search_locations:
		each_location = each_location.string
		AllLocations.append(each_location)
		#print("Movie Available Locations:",each_location)
		
	def conv_list_string(org_list, seperator=' '):
		return seperator.join(org_list)
	
	global full_str	
	full_str = conv_list_string(AllLocations, ' ; ')
	print(full_str)
	
	y = souped_resource.find('ul', 'movie-details__detail')
	x = y.find_all('li')
	a = x[3:-1]
	b = x[1]
	global type_genre
	type_genre = []


	
	for release_y in b:
		release_y = release_y.string
		global releasedate
		releasedate = release_y.replace(" ","")
		print("Movie Release Date:",releasedate)
		
	for genre_y in a:
		genre_y = genre_y.string
		type_genre.append(genre_y)
		
	print("Type of Genre:",type_genre)
		
	
	
	
CrawlWords(r'https://www.fandango.com/infidel-2020-223278/movie-overview')


EMAIL_ADDRESS = 'rebeccasanga3018@gmail.com'
EMAIL_PASSWORD = 'Password@123'

msg = EmailMessage()
msg['Subject'] = 'Fedango Movie Information'
msg['From'] = EMAIL_ADDRESS
msg['To'] = 'shivaraj0870@gmail.com'
msg.set_content("This email alerts on movie information")

msg.add_alternative("""\
<!DOCTYPE html>
<html>
<h2>Top Stock Prices</h2>
<p>Hello Raj! Greetings of the day. This email is for alerts on Tesla, Amazon and Oracle Stock Prices</p>

<table border="1" class="dataframe">
<thead>
	<tr style="text-align: right;">
		<th>Movie Name</th>
		<th>Release Date</th>
		<th>locations</th>
		<th>Genre</th>
	</tr>
</thead>
<tbody>
	<tr>		
		<th>{col1}</th>
		<td>{col2}</td>
		<td>{col3}</td>
		<td>{col4}</td>
	</tr>
	
<tbody>
</table>
</body>

</html>

""".format(col1 = movie_name,col2 = releasedate,col3 = full_str, col4 = type_genre), subtype='html')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
	smtp.send_message(msg)

