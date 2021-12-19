
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from flask import *
from flask_mysqldb import MySQL
import os
from flask_mail import Mail, Message


app = Flask(__name__)
app = Flask(__name__)
app.secret_key=os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fakenews'
mysql = MySQL(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pranitha.kandimalla123'
app.config['MAIL_PASSWORD'] = 'amma.@123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
with open('modelfinal.pickle',"rb") as file1:
    LR=pickle.load(file1)
    vectorization=pickle.load(file1)
def fake_news_det(news):
    input_data = [news]
    vectorized_input_data = vectorization.transform(input_data)
    #print(vectorized_input_data.shape)
    prediction = LR.predict(vectorized_input_data)
    if prediction[0]==1.0:
        return ['REAL']
    else:
        return ['FAKE']
@app.route('/')
def login():
    return render_template('login.html')
@app.route('/index1')
def index1():
    return render_template('index1.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        message = request.form['message']
        pred = fake_news_det(message)
        #print(pred)
        return render_template('index.html', prediction=pred)
        #return redirect(url_for('predict'))
    else:
        return render_template('index.html', prediction="Something went wrong")
@app.route('/login_validation',methods=['POST'])
def login_validation():
    error=None
    email=request.form.get('email')
    password=request.form.get('password')
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM `user` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    users=cursor.fetchall()
    cursor.close()
    mysql.connection.commit()
    #print(user)
    #user = list(map(str, users[0]))
    if len(users)>0:
        session['userid']=users[0][0]
        return redirect('/index1')
    else:
        #flash('The email or password is wrong.')
        error="Invalid credentials"
        return redirect('/')
@app.route('/contact',methods=['POST'])
def contact():
    msg = Message('feedback received from '+request.form.get('name'), sender = 'pranitha.kandimalla123@gmail.com', recipients = ['pranitha.kandimalla123@gmail.com','palurineelima2000@gmail.com'])
    msg.body = "Feedback:"+request.form.get('message')+'\nfrom mail id :  '+request.form.get('email')
    mail.send(msg)
    return render_template('index1.html')


@app.route('/add_user',methods=['post'])
def add_user():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor = mysql.connection.cursor()
    cursor.execute("""INSERT INTO `user`(`userid`,`email`,`password`)VALUES 
    (NULL,'{}','{}')""".format(email,password))
    users = cursor.fetchall()
    cursor.close()
    mysql.connection.commit()
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM `user` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['userid']=myuser[0][0]
    return redirect('/index1')
    users = cursor.fetchall()
    cursor.close()
    mysql.connection.commit()
@app.route('/logout')
def logout():
    #session.pop('userid')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)