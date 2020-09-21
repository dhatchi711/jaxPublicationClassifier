from flask import Flask, render_template, request, Response, redirect, url_for
from flask import send_file
from datetime import date
import datetime
from openpyxl import load_workbook
import io
import pandas as pd
import xlsxwriter

import pubmed_search

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
def search_select():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def result():
    start = request.form.get("start-date")
    end = request.form.get("end-date")
    authors = request.form.get("authors")
    terms = request.form.get("terms")
    ccsg = request.form.get("ccsg")
    if not start or not end or not authors or not terms or not ccsg:
        return redirect(url_for('search_select'))
    df = pubmed_search.main(start, end)
    dfName = start + "TO" + end + ".xlsx"
    df.to_excel('/Users/kgovid/PycharmProjects/jaxPublicationClassifier1/' + dfName)
    return render_template("simple.html", dataframe=df.to_html(), start=start, end=end)


@app.route('/downloadFile/<start>/<end>', methods=["POST", "GET"])
def download_file(start, end):
    start = start
    end = end
    dfName = start + "TO" + end + ".xlsx"
    print(dfName)
    directory = dfName
    print(directory)
    return send_file(filename_or_fp=directory,
                     as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
