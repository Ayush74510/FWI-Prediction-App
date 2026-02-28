import pickle
from flask import Flask,request,jsonify,render_template

app = Flask(__name__)


## Import Ridge regressor and standard scaler pickle
with open('models/ridge.pkl', 'rb') as f:
    ridge_model = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    standard_scaler = pickle.load(f)




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    try:
        if request.method == 'POST':
            Temperature = float(request.form.get('Temperature'))
            RH = float(request.form.get('RH'))
            Ws = float(request.form.get('Ws'))
            Rain = float(request.form.get('Rain'))
            FFMC = float(request.form.get('FFMC'))
            DMC = float(request.form.get('DMC'))
            ISI = float(request.form.get('ISI'))
            Classes = float(request.form.get('Classes'))
            Region = float(request.form.get('Region'))

            new_data_scaled = standard_scaler.transform(
                [[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region]]
            )
            result = ridge_model.predict(new_data_scaled)

            return render_template('home.html', result=round(result[0], 2))
        
    except Exception as e:
        return render_template('home.html',result=f'Error: {str(e)}')
    
    return render_template('home.html')
    
    
@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.json
    scaled = standard_scaler.transform([[
        data['Temperature'],
        data['RH'],
        data['Ws'],
        data['Rain'],
        data['FFMC'],
        data['DMC'],
        data['ISI'],
        data['Classes'],
        data['Region']
    ]])
    prediction = ridge_model.predict(scaled)
    return jsonify({'prediction': float(prediction[0])})
    

 
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)