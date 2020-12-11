"""
Data to extract
{
  address: "1234 Main Street", - tag = <address class="list-card-adr">0 County Road 6114, Saint Johns, AZ 85936</address>
  city: "Cochise",              -tag = <address class="list-card-adr">0 County Road 6114, Saint Johns, AZ 85936</address>
  state: "AZ",                  tag = <address class="list-card-adr">0 County Road 6114, Saint Johns, AZ 85936</address>
  zip: 12345,                   tag = <address class="list-card-adr">0 County Road 6114, Saint Johns, AZ 85936</address>
  asking_price: 90000,          tag = <div class="list-card-heading">
                                        <div class="list-card-price">$12,90000</div>
  acreage: 37.54                tag = <ul class="list-card-details">
                                        <li class="">
                                        40
                                        <abbr class="list-card-label">
                                        <!-- -->
                                        acres lot
                                        </abbr>
                                        </li>
                                        </ul>
}

'price': '$8,900',
'unformattedPrice': 8900,
'address': 'Owens Whitney Elemental District, Wikieup, AZ 85360',
'addressStreet': 'Owens Whitney Elemental District',
'addressCity': 'Wikieup',
'addressState': 'AZ',
'addressZipcode': '85360',
'lotAreaString': '20 acres'

"""

from urllib.request import Request, urlopen
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint, pformat


url = "https://www.zillow.com/az/land/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Arizona%22%2C%22mapBounds%22%3A%7B%22west%22%3A-117.85803002343751%2C%22east%22%3A-106.21252221093751%2C%22south%22%3A29.775098051053767%2C%22north%22%3A38.08088103174325%7D%2C%22mapZoom%22%3A6%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A8%2C%22regionType%22%3A2%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A20000%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22mf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A66%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22lot%22%3A%7B%22min%22%3A871200%7D%2C%22sf%22%3A%7B%22value%22%3Afalse%7D%2C%22tow%22%3A%7B%22value%22%3Afalse%7D%2C%22manu%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
header = {
	'User-Agent': 'Mozilla/5.0',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'en-US, en;q=0.9',
	'cache-control': 'max-age=0',
	'cookie': 'zguid=23|%24a272303f-4df0-4987-b19c-689a47a3d208; zgsession=1|55352809-9fd0-4972-9114-9b67314294e0; JSESSIONID=06AAB2343EDD1A47E891C956CDAFFBAA; g_state={"i_p":1607734132593,"i_l":2}; AWSALB=4wpwR9taHEV9fwz9KshCzlEk+NM44z1GGpf6AhdEM+9qvB8KY9j9qn7rRVnJR2RH1uL/cOlWnYVfBOA1ke5+inbmN2SfdOQ1Zp3CjF/ytrr4KqzdGT5nCAW2CtSH; AWSALBCORS=4wpwR9taHEV9fwz9KshCzlEk+NM44z1GGpf6AhdEM+9qvB8KY9j9qn7rRVnJR2RH1uL/cOlWnYVfBOA1ke5+inbmN2SfdOQ1Zp3CjF/ytrr4KqzdGT5nCAW2CtSH; search=6|1610240886763%7Crect%3D38.08088103174325%252C-106.21252221093751%252C29.775098051053767%252C-117.85803002343751%26rid%3D8%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26type%3Dland%26pt%3Dpmf%252Cpf%26lot%3D871200-%26price%3D0-20000%26mp%3D0-66%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%09%09%09%09%09%09%09',
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'same-origin',
	'sec-fetch-user': '?1',
	'sec-gpc': '1',
	'upgrade-insecure-requests': '1',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36'}

req = requests.get(url, headers=header)
soup = BeautifulSoup(req.text, "html.parser")
# print(soup.prettify())

results_list = []
containers = soup.find_all("div", "list-card-price")
scripts = soup.select("[type='application/json']")[1]     # cat1   queryState
# <script data-zrr-shared-data-key="mobileSearchPageStore" type="application/json"><!--{"queryState":

for results in scripts:
	stripped = results.strip("<!--")
	stripped2 = stripped.strip("-->")

	# print(stripped2)

json_results = json.loads(stripped2)["cat1"]["searchResults"]["listResults"]
# print(json_results)


def get_zillow_data():
	zillow_list = []
	for info in json_results:
		address = info["addressStreet"]
		# print(address)
		city = info["addressCity"]
		# print(city)
		state = info["addressState"]
		# print(state)
		zipcode = info["addressZipcode"]
		# print(zipcode)
		price = info["unformattedPrice"]
		# print(price)
		acreage = info["lotAreaString"]
		# print(acreage)
		zillow_data = {"address": address, "city": city, "state": state, "zipcode": str(zipcode), "price": str(price), "acreage": acreage}
		zillow_list.append(zillow_data)
	return zillow_list


print("data")
pprint(get_zillow_data())



