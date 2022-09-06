import requests
import re
from prometheus_client import Gauge

#create the Prometheus gagues
gToday = Gauge('pv_forecast_today_kwh', 'Kilowatt hours forecast to be generated today')
gTomorrow = Gauge('pv_forecast_tomorrow_kwh', 'Kilowatt hours forecast to be generated tomorrow')

#make the API call. lat/long/incline of the solar panels/azimuth/peak capacity of solar panels(kWh)
url = "https://api.forecast.solar/estimate/59.363986003121134/17.92912964578408/23/45/6.9"
response = requests.request("GET", url)
response = response.json()

#select the total estimate for today and tomorrow
daily = response['result']['watt_hours_day']

#split the results into two key-value pairs
daily = str(daily).split(',')

#split the key-value pairs at the :
dateAndwhToday = daily[0].split(':')
dateAndwhTomorrow = daily[1].split(':')

#select the second element in the list and tidy up the result a bit
whToday = int(dateAndwhToday[1])
whTomorrow = str(dateAndwhTomorrow[1])
whTomorrow = re.sub('\D', '', whTomorrow)
whTomorrow = int(whTomorrow)

#convert to kWh
kwhToday = whToday / 1000
kwhTomorrow = whTomorrow / 1000

print(kwhToday)
print(kwhTomorrow)

#set the gauges
gToday.set(kwhToday)
gTomorrow.set(kwhTomorrow)