import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import csv
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
model = pickle.load(open('xgb1.pkl','rb'))

@app.route('/')
def home():
    return render_template('index_3.html')

@app.route('/predict',methods=['GET','POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    if request.method == 'POST':
        f = request.form['csvfile']
        with open(f) as file:
            csvfile = pd.read_csv(file) #Reading the file
            csvfile = csvfile.fillna(0) #Fill na values with 0
            
            for f in csvfile.columns: #For loop to label encode all the categorical values
                if csvfile[f].dtype=='object':
                    lbl = LabelEncoder()
                    lbl.fit(list(csvfile[f].values))
                    csvfile[f] = lbl.transform(list(csvfile[f].values))
                    
            copy_file = csvfile.copy() #Creating a copy of the encoded file
            copy_file = copy_file.drop(['TransactionID'],axis=1) #Dropping transactionID column from the copy file
            
            commentsList = copy_file.values #Taking only the values from the file
        pred = model.predict(commentsList) #Predicting on the values using the model
        
    l = list() #Creating a list
    for i in range(len(pred)): #For loop to collect output as Fraud or non fraud in the list
        if pred[i]==0:
            l.append('Non Fraud')
        elif pred[i]==1:
            l.append('Fraud')
    
    data = list(zip(csvfile['TransactionID'].values,l)) #Combining the TransactionID and the prediction list
    
    output = pd.DataFrame(data, columns=['TransactionID','Predictions']) #Creating data frame to put together all the values
    output
    
    headings = output.columns
    headings = tuple(headings)
    
    d = output.values
    d = tuple(d)

    return render_template('data_3.html', headings=headings, d=d)



if __name__ == "__main__":
    app.run(debug=True)
