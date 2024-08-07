import sqlite3
from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)
app.port = 5001

@app.route('/')
def hello_world():
	return 'Hello World\n'
	
#--------------------TEMP OVEN--------------------------#

@app.route('/report/mode/<int:mode>/temp/<int:temp>/time/<time>')
def report_climate(mode, temp, time):
	
	timeStr=time.replace('T', ' ') # det gick inte att skicka strängen med mellanslag till url från arduinoIDE
	with open("data.log", "a") as filehandle:
		filehandle.write(f" Setting {mode} Temperature {temp} °C Time {timeStr}\n")	#'set' som förkortning till setting är nog ett reserverat ord i sqlite
	conn=sqlite3.connect('tc_MAX31855.db')
	conn.execute(f"INSERT INTO oven_temp VALUES({mode}, {temp}, '{timeStr}')")
	conn.commit()
	conn.close()
	
	if mode==0: #Om ugnen inte är inställd returnerar den att den inte är inställd.
		return f'Oven is not set, temperature is {temp} °C and time is {timeStr}'
	else:
		return f'Oven is set to {mode}, temperature is {temp} °C at {timeStr}'
			

@app.route('/status')
def status():
	conn = sqlite3.connect('tc_MAX31855.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * from oven_temp")
	records = cursor.fetchall()
	cursor.close()
	return render_template('result.html', results=records)


if __name__ == '__main__':
	app.debug = True
	app.run("0.0.0.0", 5001)
