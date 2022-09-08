import requests
import re
from flask_apscheduler import APScheduler
from flask import Flask, render_template, make_response, session

app = Flask(__name__)
scheduler = APScheduler()

kwhToday = 0
kwhTomorrow = 0

def getForecast():

	global kwhToday
	global kwhTomorrow

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

@scheduler.task("interval", hours=3)
def runGetForecast():
	getForecast()
scheduler.start()

@app.before_request
def before_request_func():
    getForecast()

@app.route("/metrics")
def metrics():

	resp = make_response(
        render_template(
            "metrics.html",
            metric1=kwhToday,
			metric2=kwhTomorrow
        )
    )
	resp.headers["Content-Type"] = "text/plain; version=0.0.4; charset=utf-8"
	return resp

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5205")
