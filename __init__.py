from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/commits/")
def index():
    if request.args.get('data') == 'commits':
        # Logique pour récupérer les données des commits
        url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
        response = requests.get(url)
        commits = response.json()

        commits_by_minute = {}
        for commit in commits:
            commit_date = commit['commit']['author']['date']
            date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.strftime('%Y-%m-%d %H:%M')
            commits_by_minute[minute] = commits_by_minute.get(minute, 0) + 1

        data = [{"minute": key, "count": value} for key, value in commits_by_minute.items()]
        return jsonify(data)

    # Sinon, retourner l'HTML
    return render_template("commits.html")


@app.route("/")
def hello_world():
  return render_template('hello.html') #Comm2
                                                                                                                                      
if __name__ == "__main__":
  app.run(debug=True)
