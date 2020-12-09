import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'TransactionID':3663549, 'TransactionDT':18403224, 'TransactionAmt':31.95, 'ProductCD':W, 'card1':10409, 'card2':111,'card3':150, 'card4':visa, 'card5': 226, 'card6':debit, 'addr1':170, 'addr2':87, 'dist1':1, 'dist2':0, 'P_emaildomain':gmail.com, 'R_emaildomain':0})

print(r.json())