from flask import Flask, render_template, request
from flask import redirect, url_for, abort, g
import io
import web_helper
import json
import plotly

### stuff from last class
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('introduction.html')


@app.route('/Data_preparation/', methods=['POST', 'GET'])
def Data_preparation():
    if request.method == 'GET':
        return render_template('Data_preparation.html')
    else:
        try:
            fig1 = web_helper.plotly_flights(request.form["year"])
            fig2 = web_helper.plotly_flights2(request.form["year"])
            graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
            graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('Data_preparation.html', graphJSON1=graphJSON1, graphJSON2=graphJSON2)
        except:
            return render_template('Data_preparation.html')


@app.route('/Split_Data/')
def Split_Data():
    return render_template('Split_Data.html')


@app.route('/Model_Selection/', methods=['POST', 'GET'])
def Model_Selection():
    if request.method == 'GET':
        return render_template('Model_Selection.html')
    else:
        return render_template('Model_Selection.html')


@app.route('/feedback/', methods=['POST', 'GET'])
def Feedback():
    if request.method == 'GET':
        return render_template('feedback.html')
    else:
        # if the user submits the form
        if request.form['submit_button'] == 'Submit':
            try:
                web_helper.insert_message(request)
                return render_template('feedback.html', thanks=True)
            except:
                return render_template('feedback.html', error=True)

        if request.form['submit_button'] == 'View Feedback':
            try:
                out = web_helper.view_messages() # a format html script in string form
                return render_template('feedback.html', view=out)
            except:
                return render_template('feedback.html', view_error=True)