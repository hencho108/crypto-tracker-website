from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv
import pandas as pd
from .models import Transaction
from . import db 
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('upload.html', user=current_user, table="")

@views.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    if request.method == 'POST':
        if 'confirm_data' in request.form:
            data = pd.read_sql('SELECT * FROM TempTransaction', con=db.engine) 
            data.to_sql(name='Transaction', con=db.engine, index=False, if_exists='append')
            flash('Data submitted successfully.', category='success')
            return redirect(url_for('views.my_portfolio'))
            
        else:
            csv_file = request.form['csv_file']
            data = pd.read_csv(csv_file)
            data['user_id'] = current_user.id
            data.to_sql(name='TempTransaction', con=db.engine, index=False, if_exists='replace')
            return render_template(
                'data.html', 
                data=data.to_html(
                    index=False, 
                    justify='unset', 
                    border=0,
                    na_rep=""
                ).replace('dataframe','table'), 
                user=current_user
            )


@views.route('/my-portfolio', methods=['GET', 'POST'])
@login_required
def my_portfolio():

    query = f"SELECT * FROM 'Transaction' WHERE user_id = {current_user.id}"
    data = pd.read_sql(query, con=db.engine) 
    
    return render_template(
        'my_portfolio.html', 
        data=data.to_html(
            index=False, 
            justify='unset', 
            border=0,
            na_rep=""
        ).replace('dataframe','table'), 
        user=current_user
    )