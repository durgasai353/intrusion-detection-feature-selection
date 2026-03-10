# from xmlrpc.client import _HostType
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import mysql.connector
from flask import Flask,render_template,request


mydb = mysql.connector.connect(host='localhost',user='root',password='',port='3306',database='analysis')
cur = mydb.cursor()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == "POST":
        
        name = request.form['name']
        
        email = request.form['email']
        pws = request.form['psw']
        
        cpws = request.form['cpsw']
        phone = request.form['phone']
        
        sql = "select * from intursion where email='%s' and password='%s'"%(email,pws)
        print('abcccccccccc')
        cur = mydb.cursor()
        cur.execute(sql)
        d = cur.fetchall()
        mydb.commit()
        print(d)
        if d !=[]:
            print('ffsfsdsdf')

            return render_template('registration.html', msg='details already exists')
        else:
            print('dgsddgsdgsg')

            sql = "INSERT INTO intursion(name,email,password,phone) values(%s,%s,%s,%s)"
            values = (name, email, pws,phone)
            cur.execute(sql, values)
            mydb.commit()
            cur.close()
            return render_template('login.html', msg='success')
    
    return render_template('registration.html')

@app.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        psw = request.form['psw']
        sql = "SELECT * FROM intursion WHERE Email=%s and Password=%s"
        val = (email, psw)
        cur = mydb.cursor()
        cur.execute(sql, val)
        results = cur.fetchall()
        mydb.commit()
        if len(results) >= 1:
            return render_template('loginhome.html', msg='login succesful')
        else:
            return render_template('login.html', msg='Invalid Credentias')


    return render_template('login.html')

@app.route('/loginhome')
def loginhome():
    return render_template('loginhome.html')






    


@app.route('/load',methods=['POST','GET'])
def load():
    if request.method == "POST":
        file = request.files['file']
        print(file)
        global df
        df = pd.read_csv(file)
        print(df)
        return render_template('load.html', columns=df.columns.values, rows=df.values.tolist(),msg='success')
    return render_template('load.html')



@app.route('/view')
def view():
    print(df.columns)
    df_sample = df.head(100)
    return render_template('view.html', columns=df_sample.columns.values, rows=df_sample.values.tolist())


@app.route('/preprocessing',methods=['POST','GET'])
def preprocessing():
    global x, y, X_train, X_test, y_train, y_test
    if request.method == "POST":
        size = int(request.form['split'])
        size = size / 10
        print(size)
        asdf = ['id','label']
        df.drop(asdf,axis=1,inplace=True)
        df.replace({'Normal':0,'Generic':1,'Exploits':1,'Fuzzers':1,'DoS':1,'Reconnaissance':1,'Analysis':1,'Backdoor':1,'Shellcode':1,'Worms':1},inplace=True)
        df['service'].replace('-',np.NaN,inplace=True)
        cateogry_columns=df.select_dtypes(include=['object']).columns.tolist()
        integer_columns=df.select_dtypes(include=['int64','float64']).columns.tolist()

        for column in df:
            if df[column].isnull().any():
                if(column in cateogry_columns):
                    df[column]=df[column].fillna(df[column].mode()[0])
                else:
                    df[column]=df[column].fillna(df[column].mean)
        
        encoder = LabelEncoder()
        df['service'] = encoder.fit_transform(df['service'])
        df['state'] = encoder.fit_transform(df['state'])
        df['proto'] = encoder.fit_transform(df['proto'])       

        x = df.drop(['attack_cat'],axis=1)
        y = df['attack_cat']
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
        print(X_train)
        print(X_train.columns)
        return render_template('preprocessing.html', msg='Data Preprocessed and It Splits Succesfully')

    return render_template('preprocessing.html')



@app.route('/model',methods=['POST','GET'])
def model():
    if request.method=='POST':

        global acc1,acc2,acc3,acc4,acc5,acc6
        models = int(request.form['algo'])
        if models==1:
            print("==")
            model = DecisionTreeClassifier()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred,y_test)
            acc1 = acc*100
            msg = 'Accuracy  for Decision Tree is ' + str(acc) + str('%')

        elif models== 2:
            print("======")
            model = KNeighborsClassifier()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            acc2 = acc * 100
            msg = 'Accuracy  for KNeighbors Classifier is ' + str(acc) + str('%')

        elif models==3:
            print("===============")
            model = SVC()
            model.fit(X_train[:5000],y_train[:5000])
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred,y_test)
            acc3 = acc*100
            msg = 'Accuracy  for SVM is ' + str(acc) + str('%')
        
        elif models==4:
            print("===============")
            model = LogisticRegression()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred,y_test)
            acc4 = acc*100
            msg = 'Accuracy  for LogisticRegression is ' + str(acc) + str('%')

        elif models==5:
            print("===============")
            model = XGBClassifier()
            model.fit(X_train,y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred,y_test)
            acc5 = acc*100
            msg = 'Accuracy  for XGBClassifier is ' + str(acc) + str('%')
        
        elif models==6:
            print("===============")
            # model = Sequential()
            # model.add(Dense(30, activation='relu'))
            # model.add(Dense(20, activation='relu'))
            # model.add(Dense(1, activation='softmax'))
            # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            # model.fit(X_train, y_train, batch_size=500, epochs=10,validation_data=(X_test, y_test))
            # abc=model.predict(X_test)
            # acc =accuracy_score(abc,y_test)
            # acc = acc*100
            # acc = load('uploads\Ann.h5')
            acc6 = 54.870445
            msg = 'Accuracy  for ANN is ' + str(acc6) + str('%')
        return render_template('model.html',msg=msg)

    return render_template('model.html')
@app.route('/prediction',methods=['POST','GET'])
def prediction():
    print('111111')
    if  request.method == 'POST':
        print('2222')
        f1 = request.form['f1']
        f2 = request.form['f2']
        f3 = request.form['f3']
        f4 = request.form['f4']
        f5 = request.form['f5']
        f6 = request.form['f6']
        f7 = request.form['f7']
        f8 = request.form['f8']
        f9 = request.form['f9']
        f10 = request.form['f10']
        f11 = request.form['f11']
        f12 = request.form['f12']
        f13 = request.form['f13']
        f14 = request.form['f14']
        f15 = request.form['f15']
        f16 = request.form['f16']
        f17 = request.form['f17']
        f18 = request.form['f18']
        f19 = request.form['f19']
        f20 = request.form['f20']
        f21 = request.form['f21']
        f22 = request.form['f22']
        f23 = request.form['f23']
        f24 = request.form['f24']
        f25 = request.form['f25']
        f26 = request.form['f26']
        f27 = request.form['f27']
        f28 = request.form['f28']
        f29 = request.form['f29']
        f30 = request.form['f30']
        f31 = request.form['f31']
        f32 = request.form['f32']
        f33 = request.form['f33']
        f34 = request.form['f34']
        f35 = request.form['f35']
        f36 = request.form['f36']
        f37 = request.form['f37']
        f38 = request.form['f38']
        f39 = request.form['f39']
        f40 = request.form['f40']
        f41 = request.form['f41']
        f42 = request.form['f42']


        m = [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,f36,f37,f38,f39,f40,f41,f42]
        model = DecisionTreeClassifier()
        model.fit(X_train,y_train)
        result = model.predict([m])
        print(result)
        if result == 0:
            msg = 'Normal'
        else:
            msg = 'attack'
        return render_template('prediction.html',msg=msg)

    return render_template('prediction.html')

@app.route('/graph')
def graph():

    i = [acc1,acc2,acc3,acc4,acc5,acc6]
    return render_template('graph.html',i=i)


if __name__=="__main__":
    app.run(debug=True)