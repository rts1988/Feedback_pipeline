from flask import Flask, render_template, url_for
import pandas as pd
from  analysis import *

print(pd.__version__)
#print(Flask.__version__)

nstudy_data = dict()
nstudy_data['highlight_filename'] = "export_5534963e-049d-453a-9dab-93b911e9ece1_highlight_2021-08-04T18_13_46.716Z.csv"
nstudy_data['terms_filename'] = "export_5534963e-049d-453a-9dab-93b911e9ece1_term_2021-08-04T18_16_02.505Z.csv"
nstudy_data['notes_filename'] = "export_5534963e-049d-453a-9dab-93b911e9ece1_note_2021-08-04T18_14_43.718Z.csv"
user_id = "8e588dfd-c08a-4bb8-8a76-756dd4dab060"


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',paragraph=get_analysis_report(nstudy_data,user_id))
    #return render_template('index.html',  tables=[data2.to_html(classes='data')], titles=data2.columns.values)

if __name__=="__main__":
    app.run(debug=True)
