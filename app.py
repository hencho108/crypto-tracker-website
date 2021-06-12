from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import csv

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('upload.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        f = request.form['csv_file']
        data = []
        with open(f) as file:
            csv_file = csv.reader(file)
            for row in csv_file:
                data.append(row)
        data = pd.DataFrame(data)
        return render_template('data.html', data=data.to_html(header=False, index=False))

if __name__ == '__main__':
    app.run(debug=True)




