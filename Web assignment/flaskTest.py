from flask import Flask, render_template, request
from datetime import datetime
import sqlite3 as mydb
app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('tempSite.html')

@app.route('/',methods=['POST'])
def Print():
    if request.method=='POST':
        firstDate=request.form['firstDate']
        lastDate=request.form['lastDate']
      
        firstTemp = datetime.strptime(firstDate,'%Y-%m-%d')
        lastTemp = datetime.strptime(lastDate,'%Y-%m-%d')
        searchFirst = firstTemp.strftime('%m/%d/%Y')
        searchLast = lastTemp.strftime('%m/%d/%Y')
        
        conn = mydb.connect('/home/pi/ClassCode/HW1/temperature.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM TempData WHERE date_time BETWEEN ? AND ?', (searchFirst, searchLast,))
        
    return render_template('tempSite.html', data=cursor.fetchall(),firstDate=firstDate, lastDate=lastDate)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)