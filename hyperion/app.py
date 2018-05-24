# -*- coding: utf-8 -*-
#!flask/bin/python
import json

import psycopg2
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from psycopg2.extras import RealDictCursor

connect_str = "dbname='hyperion' user='qa' host='10.250.0.62' " + \
              "password='qa'"
app = Flask(__name__)
auth = HTTPBasicAuth()

@app.route('/invoices', methods=['GET'])
def get_invoices():
    conn = psycopg2.connect(connect_str)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT
        id,data
        FROM invoice
        LIMIT 1000
    """)
    result = cur.fetchall()
    conn.close()
    return jsonify({'result': json.dumps(result, indent=2)}), 200


@app.route('/receiver', methods=['POST'])
def insert_invoice():
    data = {
        'data': request.json
    }
    conn = psycopg2.connect(connect_str)
    cur = conn.cursor()
    cur.execute("""
         insert into invoice ( data ) VALUES (%s);
     """, (json.dumps(data),))
    conn.commit()
    conn.close()
    return jsonify({'result': 'success'}), 201


@app.route('/invoices/<string:uuid>', methods=['GET'])
def get_invoice_by_uuid(uuid):
    conn = psycopg2.connect(connect_str)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("select data from invoice where data #> '{data,uuid}'='\"" + uuid + "\"';")
    result = cur.fetchall()
    conn.close()
    return jsonify({'result': json.dumps(result, indent=2)}), 200


if __name__ == '__main__':
    app.run(debug=False, port=5000)
