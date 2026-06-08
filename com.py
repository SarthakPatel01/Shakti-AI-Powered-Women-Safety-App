
# ______________________________________________________________________________________________________________






import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import pymysql
import base64
import numpy as np
import cv2
import threading
import webbrowser
from datetime import datetime

# app

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

print(" Server Started...")


def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Jaga@654321",
        database="sakti_safe",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# map
def show_popup(message, lat, lon):
    try:
        from plyer import notification
        notification.notify(
            title=" EMERGENCY ALERT",
            message=f"{message}\nLat: {lat}, Lon: {lon}",
            timeout=10
        )
    except Exception as e:
        print("Popup error:", e)

def open_map(lat, lon):
    try:
        url = f"https://www.google.com/maps?q={lat},{lon}"
        webbrowser.open(url)
    except Exception as e:
        print("Map error:", e)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (fullname, phone, email, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get("fullname"),
            data.get("phone"),
            data.get("email"),
            data.get("username"),
            data.get("password")
        ))

        return jsonify({"status": "success"})

    except Exception as e:
        print("Signup Error:", e)
        return jsonify({"status": "error", "message": str(e)})

    finally:
        db.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("""
            SELECT id, fullname, phone, email, username 
            FROM users 
            WHERE username=%s AND password=%s
        """, (data.get("username"), data.get("password")))

        user = cursor.fetchone()

        if user:
            return jsonify({
                "status": "success",
                "user": user
            })

        return jsonify({"status": "fail"})

    except Exception as e:
        print("Login Error:", e)
        return jsonify({"status": "error"})

    finally:
        db.close()


@app.route('/emergency_alert', methods=['POST'])
def emergency_alert():
    data = request.get_json()

    db = get_db()
    cursor = db.cursor()

    try:
        lat = float(data.get("latitude"))
        lon = float(data.get("longitude"))
        message = data.get("message", "Emergency")
        time_str = data.get("time")

        
        try:
            formatted_time = datetime.strptime(
                time_str, "%Y-%m-%d %H:%M:%S.%f"
            ).strftime("%d %b %Y, %I:%M %p")
        except:
            formatted_time = time_str

        # output
        print("\n========== EMERGENCY ALERT ==========")
        print(f"Location : {lat:.6f}, {lon:.6f}")
        print(f"Map Link : https://www.google.com/maps?q={lat},{lon}")
        print(f"Message  : {message}")
        print(f"Time     : {formatted_time}")
        print("========================================\n")

        # save to database
        cursor.execute("""
            INSERT INTO alerts (latitude, longitude, message, time)
            VALUES (%s, %s, %s, %s)
        """, (lat, lon, message, formatted_time))

        # 
        threading.Thread(target=show_popup, args=(message, lat, lon)).start()
        threading.Thread(target=open_map, args=(lat, lon)).start()

        return jsonify({"status": "success"})

    except Exception as e:
        print(" ALERT ERROR:", e)
        return jsonify({"status": "error", "message": str(e)})

    finally:
        db.close()



@socketio.on('connect')
def connect():
    print(" CLIENT CONNECTED")

@socketio.on('disconnect')
def disconnect():
    print(" CLIENT DISCONNECTED")

#camera stream
cv2.namedWindow(" SAKTI LIVE", cv2.WINDOW_NORMAL)
cv2.resizeWindow(" SAKTI LIVE", 800, 600)

@socketio.on('video')   
def handle_video(data):
    try:
        print("FRAME RECEIVED")

        image_data = data.get("image")

        if not image_data:
            return

        img_bytes = base64.b64decode(image_data)

        frame = cv2.imdecode(
            np.frombuffer(img_bytes, np.uint8),
            cv2.IMREAD_COLOR
        )

        if frame is None:
            print(" Decode failed")
            return

        
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

        cv2.imshow(" SAKTI LIVE", frame)
        cv2.waitKey(1)

    except Exception as e:
        print(" Video Error:", e)


if __name__ == '__main__':
    print("🌐 Running on http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)