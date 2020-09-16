from flask import Flask, render_template, request, Response, redirect, url_for
from flask import send_file
from datetime import date
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


@app.route('/search', methods=["POST"])
def search():
    author = request.form.get("author")
    term = request.form.get("term")
    ccsg = request.form.get("ccsg")
    if not author or not term or not ccsg:
        return render_template('resubmit.html')
    return render_template('datepicker.html')


@app.route('/download', methods=["POST"])
def download():
    start = request.form.get("start-date")
    end = request.form.get("end-date")
    if not start or not end:
        return render_template('datepicker.html')
    df = pubmed_search.main(start, end)
    return render_template("simple.html", dataframe=df.to_html(), start=start, end=end)


@app.route('/downloadFile/<start>/<end>', methods=["POST", "GET"])
def download_file(start, end):
    start = start
    end = end
    df = pubmed_search.main(start, end)
    headerFile = "attachment; filename= " + 'publicationsFor' + start + end + ".csv"
    return Response(
        df.to_csv(),
        mimetype="text/csv", headers={"Content-disposition": headerFile})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
