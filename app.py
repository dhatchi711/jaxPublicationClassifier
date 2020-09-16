from flask import Flask, render_template, request, Response
from flask import send_file
from datetime import date
from openpyxl import load_workbook
import io
import pandas as pd
import xlsxwriter

import pubmed_search

app = Flask(__name__)
app.secret_key = 'secret'
author = ''
ccsg = ''
term = ''
start = ''
end = ''


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


@app.route('/datepicker', methods=["POST"])
def datepick():
    start = request.form.get("trip-start")
    end = request.form.get("trip-end")
    if not start or not end:
        return "failure"
    df = pubmed_search.main(start, end)
    return render_template("simple.html", dataframe=df.to_html())

    #return render_template('simple.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

#old way 2.0
"""
    return Response(
        df.to_csv(),
        mimetype="text/csv", headers={"Content-disposition": "attachment; filename=filename.csv"})
#old way 1.0
    strIO = io.BytesIO()
    excel_writer = pd.ExcelWriter(strIO, engine="xlsxwriter")
    df.to_excel(excel_writer, sheet_name="sheet1")
    excel_writer.save()
    excel_data = strIO.getvalue()
    
    strIO.seek(0)

    return send_file(strIO,
                     attachment_filename='listOfPublications.xlsx',
                     as_attachment=True)
    """


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
