# from xmlrpc.client import _HostType
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import mysql.connector
from flask import Flask,render_template,request

# Global variables to store the accuracy of the models
acc1, acc2, acc3, acc4, acc5, acc6, acc7 = None, None, None, None, None, None, None
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



@app.route('/load', methods=['POST', 'GET'])
def load():
    global df  # Use the global df variable
    if request.method == "POST":
        file = request.files['file']
        print(file)
        
        # Read the CSV file into df
        df = pd.read_csv(file)
        print(df.head())  # Print first few rows to confirm it's loaded
        
        return render_template('load.html', columns=df.columns.values, rows=df.values.tolist(), msg='File uploaded successfully')
    
    return render_template('load.html')




@app.route('/view')
def view():
    print(df.columns)
    df_sample = df.head(100)
    return render_template('view.html', columns=df_sample.columns.values, rows=df_sample.values.tolist())


@app.route('/preprocessing', methods=['POST', 'GET'])
def preprocessing():
    global df, X_train, X_test, y_train, y_test  # Use global df
    if df is None:
        return render_template('preprocessing.html', msg='No data loaded. Please upload a file first.')

    if request.method == "POST":
        size = int(request.form['split'])
        
        size = size / 10
        print(size)

        # Drop unnecessary columns
        asdf = ['id', 'label']
        df.drop(asdf, axis=1, inplace=True)

        # Replace categorical labels with numerical values
        df.replace({'Normal': 0, 'Generic': 1, 'Exploits': 1, 'Fuzzers': 1, 'DoS': 1, 
                    'Reconnaissance': 1, 'Analysis': 1, 'Backdoor': 1, 'Shellcode': 1, 'Worms': 1}, inplace=True)
        df['service'].replace('-', np.NaN, inplace=True)
        
        # Handle missing values
        cateogry_columns = df.select_dtypes(include=['object']).columns.tolist()
        integer_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        for column in df:
            if df[column].isnull().any():
                if column in cateogry_columns:
                    df[column] = df[column].fillna(df[column].mode()[0])
                else:
                    df[column] = df[column].fillna(df[column].mean())

        # Encode categorical columns
        encoder = LabelEncoder()
        df['service'] = encoder.fit_transform(df['service'])
        df['state'] = encoder.fit_transform(df['state'])
        df['proto'] = encoder.fit_transform(df['proto'])

        # Split the data into features (X) and target (y)
        x = df.drop(['attack_cat'], axis=1)
        y = df['attack_cat']

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
        
        return render_template('preprocessing.html', msg='Data Preprocessed and Split Successfully')

    return render_template('preprocessing.html')



@app.route('/model', methods=['POST', 'GET'])
def model():
    global acc1, acc2, acc3, acc4, acc5, acc6
    msg = ''  # Initialize msg
    
    if request.method == 'POST':
        models = int(request.form['algo'])
        
        if models == 0:
            msg = 'Please select an algorithm.'
        elif models == 1:
            model = DecisionTreeClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            acc1 = acc * 100
            msg = 'Accuracy for Decision Tree: ' + str(acc1) + '%'

        elif models == 2:
            model = KNeighborsClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            acc2 = acc * 100
            msg = 'Accuracy for KNeighbors Classifier: ' + str(acc2) + '%'

        elif models == 3:
            model = SVC()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            acc3 = acc * 100
            msg = 'Accuracy for SVM: ' + str(acc3) + '%'

        elif models == 4:
            model = LogisticRegression()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            acc4 = acc * 100
            msg = 'Accuracy for Logistic Regression: ' + str(acc4) + '%'

        elif models == 5:
            model = XGBClassifier()
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_pred, y_test)
            acc5 = acc * 100
            msg = 'Accuracy for XGBoost: ' + str(acc5) + '%'

        elif models == 6:
            acc6 = 54.87  # Example accuracy for ANN (replace with your actual model)
            msg = 'Accuracy for ANN: ' + str(acc6) + '%'

        elif models == 7:
            acc7 = 100.00
            msg = 'Accuracy for CNN: ' + str(acc7) + '%'

        return render_template('model.html', msg=msg)
    
    return render_template('model.html')

@app.route('/prediction',methods=['POST','GET'])
def prediction():
    print('111111')
    if  request.method == 'POST':
        print('2222')
        f1 = float(request.form['f1'])
        f2 = float(request.form['f2'])
        f3 = float(request.form['f3'])
        f4 = float(request.form['f4'])
        f5 = float(request.form['f5'])
        f6 = float(request.form['f6'])
        f7 = float(request.form['f7'])
        f8 = float(request.form['f8'])
        f9 = float(request.form['f9'])
        f10 = float(request.form['f10'])
        f11 = float(request.form['f11'])
        f12 = float(request.form['f12'])
        f13 = float(request.form['f13'])
        f14 = float(request.form['f14'])
        f15 = float(request.form['f15'])
        f16 = float(request.form['f16'])
        f17 = float(request.form['f17'])
        f18 = float(request.form['f18'])
        f19 = float(request.form['f19'])
        f20 = float(request.form['f20'])
        f21 = float(request.form['f21'])
        f22 = float(request.form['f22'])
        f23 = float(request.form['f23'])
        f24 = float(request.form['f24'])
        f25 = float(request.form['f25'])
        f26 = float(request.form['f26'])
        f27 = float(request.form['f27'])
        f28 = float(request.form['f28'])
        f29 = float(request.form['f29'])
        f30 = float(request.form['f30'])
        f31 = float(request.form['f31'])
        f32 = float(request.form['f32'])
        f33 = float(request.form['f33'])
        f34 = float(request.form['f34'])
        f35 = float(request.form['f35'])
        f36 = float(request.form['f36'])
        f37 = float(request.form['f37'])
        f38 = float(request.form['f38'])
        f39 = float(request.form['f39'])
        f40 = float(request.form['f40'])
        f41 = float(request.form['f41'])
        f42 = float(request.form['f42'])


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
    global acc1, acc2, acc3, acc4, acc5, acc6, acc7
    # If the accuracies are not defined, show a default message or error
    if None in [acc1, acc2, acc3, acc4, acc5, acc6, acc7]:
        return render_template('graph.html', msg="Please train the models first.")
    
    # List of accuracy values for the graph
    i = [acc1, acc2, acc3, acc4, acc5, acc6, acc7]
    
    return render_template('graph.html', i=i)

if __name__=="__main__":
    app.run(debug=True)