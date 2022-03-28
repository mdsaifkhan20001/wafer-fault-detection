# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
from wsgiref import simple_server
import os

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user

            RM = float(request.form['RM'])

            PTRATIO = float(request.form['PTRATIO'])
            LSTAT = float(request.form['LSTAT'])

            filename = 'finalized_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb'))
            # loading the model file from the storage
            # predictions using the loaded model file

            prediction=loaded_model.predict([[RM,PTRATIO,LSTAT]])
            print('prediction PRICE is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=round(10000*prediction[0]))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    port = int(os.getenv("PORT"))    # port = int(os.getenv("PORT",6000))  for local Run
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host,port=port, app=app)
    httpd.serve_forever()