# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import mysql.connector

# app = Flask(__name__)
# CORS(app)

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Jaga@654321",
#     database="shakti_safe_mode"
# )

# cursor = db.cursor()

# # SIGNUP API
# @app.route('/signup', methods=['POST'])
# def signup():

#     data = request.json

#     fullname = data['fullname']
#     phone = data['phone']
#     email = data['email']
#     username = data['username']
#     password = data['password']

#     query = "INSERT INTO users (fullname,phone,email,username,password) VALUES (%s,%s,%s,%s,%s)"
#     values = (fullname,phone,email,username,password)

#     cursor.execute(query,values)
#     db.commit()

#     return jsonify({"status":"success"})


# # LOGIN API
# @app.route('/login', methods=['POST'])
# def login():

#     data = request.json
#     username = data['username']
#     password = data['password']

#     query = "SELECT * FROM users WHERE username=%s AND password=%s"
#     values = (username,password)

#     cursor.execute(query,values)
#     user = cursor.fetchone()

#     if user:
#         return jsonify({"status":"success"})
#     else:
#         return jsonify({"status":"failed"})


# if __name__ == "__main__":
#     app.run(host="0.0.0.0",port=5000)










from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jaga@654321",  
    database="shakti_safe_mode"
)

cursor = db.cursor()

# api
@app.route('/signup', methods=['POST'])
def signup():

    data = request.get_json()

    fullname = data['fullname']
    phone = data['phone']
    email = data['email']
    username = data['username']
    password = data['password']

    try:
        sql = "INSERT INTO users (fullname,phone,email,username,password) VALUES (%s,%s,%s,%s,%s)"
        val = (fullname, phone, email, username, password)

        cursor.execute(sql, val)
        db.commit()

        return jsonify({"status": "success"})

    except:
        return jsonify({"status": "error"})


# api
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    username = data['username']
    password = data['password']

    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    val = (username, password)

    cursor.execute(sql, val)

    user = cursor.fetchone()

    if user:

        return jsonify({
            "status": "success",
            "user": {
                "id": user[0],
                "fullname": user[1],
                "phone": user[2],
                "email": user[3],
                "username": user[4]
            }
        })

    else:
        return jsonify({"status": "failed"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)