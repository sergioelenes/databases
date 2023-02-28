from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_basicauth import BasicAuth
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
import pandas as pd
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:41eb9838f37947cd820249d7c4df4a26@198.251.66.139:13020/bradexpenses'
db = SQLAlchemy(app)
app.secret_key = "Macarenas"
basic_auth = BasicAuth(app)
app.config['BASIC_AUTH_USERNAME'] = 'brad'
app.config['BASIC_AUTH_PASSWORD'] = 'keonda'

class expenses(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        month = db.Column(db.String(50))
        concept = db.Column(db.String(50))
        amount = db.Column(db.Float)
        notes = db.Column(db.String(50))

#def creartabla():
#        db.session.execute("""
#                        CREATE TABLE IF NOT EXISTS expenses (
#                        id SERIAL PRIMARY KEY,
#                        month VARCHAR(50) NOT NULL, 
#                        concept VARCHAR(50) NOT NULL,
#                        amount FLOAT(50) NOT NULL,
#                        notes VARCHAR(50) NOT NULL
#                        )""")
#        db.session.commit()

#creartabla()

@app.route("/", methods=['GET','POST'])
@basic_auth.required
def loginroute():
        return render_template('index.html')

@app.route("/datain", methods=['POST'])
def datain():
    if request.method == 'POST':
        month = request.form['month']
        if month=='Month Select':
                flash('information incomplete, please try again')
                return render_template('index.html')
        concept = request.form['concept']
        if concept == 'Expense Concept':
                flash('information incomplete, please try again')
                return render_template('index.html')                
        amount = request.form['amount']
        if amount == "":
                flash('information incomplete, please try again')
                return render_template('index.html')  
        datainput = expenses(month = request.form['month'], concept = request.form['concept'],amount = request.form['amount'], notes = request.form['notes'])
        db.session.add(datainput)
        db.session.commit()
        return render_template('index.html')

@app.route("/reports", methods=['GET','POST'])
@basic_auth.required
def reports():
        return render_template('reports.html')

@app.route("/year", methods=['GET','POST'])
@basic_auth.required
def year():
        try:
                engine =  sqlalchemy.create_engine('postgresql://postgres:41eb9838f37947cd820249d7c4df4a26@198.251.66.139:13020/bradexpenses')
                df = pd.read_sql('expenses', engine)
                df.style.format({'amount':'${.2f}'})
                pivot = df.pivot_table(values='amount', index='concept', columns='month', aggfunc='sum', fill_value="-", margins=True, margins_name='Total')
                #pivot.style.format({'amount':'${00:,00f}'})
                df.to_csv('dbases/alldata.csv', header=True, index=False)
                return render_template('reports.html', tables=[pivot.to_html()], titles=[''] )
        except ValueError:
                return render_template('reports.html')


@app.route("/bymonth", methods=['GET','POST'])
@basic_auth.required
def bymonth():
        if request.method == 'POST':
                engine =  sqlalchemy.create_engine('postgresql://postgres:41eb9838f37947cd820249d7c4df4a26@198.251.66.139:13020/bradexpenses')
                mess = request.form['elmess']
                dflogstotal = pd.read_sql('expenses', engine, index_col=3)
                pormes = dflogstotal[(dflogstotal['month']==mess)]
                return render_template('reports.html', tables=[pormes.to_html()], titles=[''] )

@app.route("/alldata", methods=['GET','POST'])
@basic_auth.required
def alldata():
        expenselist = expenses.query.all()
        engine =  sqlalchemy.create_engine('postgresql://postgres:41eb9838f37947cd820249d7c4df4a26@198.251.66.139:13020/bradexpenses')
        df = pd.read_sql('expenses', engine)
        df.to_csv('dbases/alldata.csv', header=True, index=False)
        return render_template('alldata.html', expenses=expenselist)

@app.route("/delete/<id>")
@basic_auth.required
def delete(id):
        expense = expenses.query.filter_by(id=int(id)).delete()
        db.session.commit()
        return redirect(url_for('alldata'))

@app.route('/downloadxls')
@basic_auth.required
def downloadxls ():
        alldata = "/root/bdatos/alldata.csv"
        return send_file(alldata, as_attachment=True)


if __name__=='__main__':
        app.run(debug=True)