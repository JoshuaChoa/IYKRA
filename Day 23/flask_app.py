from flask import Flask, request, jsonify #To handle the communication
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib #To open imported model in the server

app = Flask(__name__)

model = joblib.load(open('/home/gmdr999/mysite/model_xgb.pkl','rb'))

@app.route('/api',methods=['POST'])

def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    
    # Transform JSON into DataFrame
    data = pd.DataFrame.from_dict(data)
    
    def age_group(age):
        if age < 35:
            return 'Productive'
        if age < 50:
            return 'Mature'
        else:
            return 'Old'
    
    # Apply function of age_group to DataFrame
    data['age_group'] = data['age'].apply(age_group)
    
    # Prepare data by teir data types
    dummy = data.select_dtypes(exclude = ['int', 'int64', 'float64'])
    integer = data.select_dtypes(include = ['int', 'int64', 'float64'])
    
    # Do OHE on dummy
    dummy2 = pd.get_dummies(dummy, drop_first = True)
    
    # Join the data from the integer part and also the OHE part
    data = pd.concat([integer, dummy2], axis = 1)
    
    # Setup StandardScaler
    SC = StandardScaler()
    
    #Do StandardScaler to Data
    data = SC.fit_transform(data)

    # Make prediction using model loaded from disk as per the data.
    prediction = model.predict(data)

    # Take the first value of prediction
    output = prediction.tolist()

    return jsonify(output)