from flask import Flask, request, jsonify
from datetime import datetime
import threading
import webbrowser

app = Flask(__name__)

# 🔔 Desktop Notification (optional)
def show_popup(message, lat, lon):
    try:
        from plyer import notification
        notification.notify(
            title="🚨 EMERGENCY ALERT",
            message=f"{message}\nLat: {lat}, Lon: {lon}",
            timeout=10
        )
    except Exception as e:
        print("Popup not available:", e)

# 🌍 Open Google Maps
def open_map(lat, lon):
    try:
        url = f"https://www.google.com/maps?q={lat},{lon}"
        webbrowser.open(url)
    except Exception as e:
        print("Map error:", e)

# 🚨 MAIN API
@app.route('/emergency_alert', methods=['POST'])
def emergency_alert():
    try:
        data = request.get_json()

        latitude = data.get("latitude")
        longitude = data.get("longitude")
        message = data.get("message")
        time = data.get("time")

        print("\n========== 🚨 EMERGENCY ALERT RECEIVED 🚨 ==========")
        print(f"📍 Location : {latitude}, {longitude}")
        print(f"💬 Message  : {message}")
        print(f"⏰ Time     : {time}")
        print("===================================================\n")

        # Run popup + map in background threads
        threading.Thread(
            target=show_popup,
            args=(message, latitude, longitude)
        ).start()

        threading.Thread(
            target=open_map,
            args=(latitude, longitude)
        ).start()

        return jsonify({
            "status": "success",
            "message": "Alert received successfully"
        }), 200

    except Exception as e:
        print("❌ Server Error:", e)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 🟢 Run Server
if __name__ == '__main__':
    print("🚀 Server running at http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)


















# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import base64
# import cv2
# import numpy as np
# import os
# from datetime import datetime

# app = Flask(__name__)
# CORS(app)

# # Folder to store frames
# SAVE_FOLDER = "frames"
# os.makedirs(SAVE_FOLDER, exist_ok=True)

# # =========================
# # 🚨 SOS ALERT API
# # =========================
# @app.route('/emergency_alert', methods=['POST'])
# def emergency_alert():
#     data = request.json

#     print("\n🚨 EMERGENCY ALERT RECEIVED 🚨")
#     print("Latitude:", data.get("latitude"))
#     print("Longitude:", data.get("longitude"))
#     print("Message:", data.get("message"))
#     print("Time:", data.get("time"))

#     # Google Maps link
#     lat = data.get("latitude")
#     lon = data.get("longitude")
#     maps_link = f"https://www.google.com/maps?q={lat},{lon}"
#     print("📍 Open location:", maps_link)

#     return jsonify({"status": "SOS received"}), 200


# # =========================
# # 📸 CAMERA STREAM API
# # =========================
# @app.route('/video_stream', methods=['POST'])
# def video_stream():
#     try:
#         data = request.json
#         image_data = data['image']

#         # Decode base64 image
#         img_bytes = base64.b64decode(image_data)
#         np_arr = np.frombuffer(img_bytes, np.uint8)
#         frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#         # Show live stream (server side)
#         cv2.imshow("📡 Live Stream", frame)
#         cv2.waitKey(1)

#         # Save frame (optional)
#         filename = os.path.join(
#             SAVE_FOLDER,
#             f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
#         )
#         cv2.imwrite(filename, frame)

#         return jsonify({"status": "frame received"}), 200

#     except Exception as e:
#         print("❌ Error:", e)
#         return jsonify({"error": str(e)}), 500


# # =========================
# # 🟢 RUN SERVER
# # =========================
# if __name__ == '__main__':
#     print("🚀 Server running on http://0.0.0.0:5000")
#     app.run(host='0.0.0.0', port=5000, debug=True)



















# import asyncio
# import websockets
# import base64
# import cv2
# import numpy as np
# import json
# import webbrowser

# print("🚀 Server Started...")

# connected_clients = set()

# # =========================
# # 📡 HANDLE CLIENT
# # =========================
# async def handler(websocket):
#     print("📱 Client connected")
#     connected_clients.add(websocket)

#     try:
#         async for message in websocket:

#             try:
#                 data = json.loads(message)

#                 # =========================
#                 # 📡 VIDEO STREAM
#                 # =========================
#                 if data["type"] == "video":
#                     img_bytes = base64.b64decode(data["image"])
#                     np_arr = np.frombuffer(img_bytes, np.uint8)
#                     frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#                     if frame is not None:
#                         cv2.imshow("📡 LIVE STREAM", frame)
#                         cv2.waitKey(1)

#                 # =========================
#                 # 🚨 SOS ALERT
#                 # =========================
#                 elif data["type"] == "sos":
#                     print("\n🚨 SOS ALERT RECEIVED 🚨")
#                     print(data)

#                     lat = data.get("latitude")
#                     lon = data.get("longitude")

#                     if lat and lon:
#                         url = f"https://www.google.com/maps?q={lat},{lon}"
#                         print("🌍 Opening location:", url)
#                         webbrowser.open(url)

#             except Exception as e:
#                 print("❌ Error processing message:", e)

#     except websockets.exceptions.ConnectionClosed:
#         print("❌ Client disconnected")

#     finally:
#         connected_clients.remove(websocket)


# # =========================
# # 🟢 RUN SERVER
# # =========================
# async def main():
#     async with websockets.serve(handler, "0.0.0.0", 5000):
#         print("🌐 WebSocket running on ws://0.0.0.0:5000")
#         await asyncio.Future()  # run forever


# asyncio.run(main())








# ___________________________________________________________________________________________________________________________________________
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_socketio import SocketIO
# import base64
# import cv2
# import numpy as np
# import webbrowser

# app = Flask(__name__)
# CORS(app)

# # 🔥 IMPORTANT: use threading (more stable)
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# print("🚀 Server started...")

# # =========================
# # 🚨 SOS API (FROM FLUTTER)
# # =========================
# @app.route('/emergency_alert', methods=['POST'])
# def emergency_alert():
#     data = request.json

#     print("\n🚨 SOS ALERT RECEIVED 🚨")
#     print(data)

#     lat = data.get("latitude")
#     lon = data.get("longitude")

#     if lat and lon:
#         maps_url = f"https://www.google.com/maps?q={lat},{lon}"
#         print("📍 Opening location:", maps_url)

#         # 🔥 AUTO OPEN MAP IN BROWSER
#         webbrowser.open(maps_url)

#     return jsonify({"status": "SOS received"}), 200


# # =========================
# # 📡 WEBSOCKET CONNECTION
# # =========================
# @socketio.on('connect')
# def connect():
#     print("✅ Client connected")


# @socketio.on('disconnect')
# def disconnect():
#     print("❌ Client disconnected")


# # =========================
# # 📸 RECEIVE CAMERA STREAM
# # =========================
# @socketio.on('message')  # Flutter sends via channel.sink.add()
# def handle_video(message):
#     try:
#         data = message

#         if isinstance(data, str):
#             import json
#             data = json.loads(data)

#         if data.get("type") == "video":
#             image_data = data.get("image")

#             # Decode base64 → image
#             img_bytes = base64.b64decode(image_data)
#             np_arr = np.frombuffer(img_bytes, np.uint8)
#             frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#             if frame is None:
#                 print("❌ Frame decode failed")
#                 return

#             # 🔥 SHOW LIVE VIDEO
#             cv2.imshow("📡 LIVE CAMERA STREAM", frame)
#             cv2.waitKey(1)

#     except Exception as e:
#         print("❌ Error:", e)


# # =========================
# # 🚨 OPTIONAL: SOS VIA SOCKET
# # =========================
# @socketio.on('sos')
# def handle_socket_sos(data):
#     print("\n🚨 SOS (WebSocket) RECEIVED")
#     print(data)

#     lat = data.get("latitude")
#     lon = data.get("longitude")

#     if lat and lon:
#         webbrowser.open(f"https://www.google.com/maps?q={lat},{lon}")


# # =========================
# # 🟢 RUN SERVER
# # =========================
# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)



#     # ____________________________________________________________________________________________________






# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_socketio import SocketIO
# import base64
# import cv2
# import numpy as np
# import webbrowser
# import json

# app = Flask(__name__)
# CORS(app)

# # ✅ Use threading (more stable than eventlet)
# socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# print("🚀 Server started on http://0.0.0.0:5000")

# # =========================
# # 🚨 SOS ALERT (BUTTON + VOICE)
# # =========================
# @app.route('/emergency_alert', methods=['POST'])
# def emergency_alert():
#     data = request.json

#     print("\n🚨 EMERGENCY ALERT RECEIVED 🚨")
#     print("📍 Latitude:", data.get("latitude"))
#     print("📍 Longitude:", data.get("longitude"))
#     print("💬 Message:", data.get("message"))
#     print("⏰ Time:", data.get("time"))

#     lat = data.get("latitude")
#     lon = data.get("longitude")

#     # 🔥 Open Google Maps automatically
#     if lat and lon:
#         maps_url = f"https://www.google.com/maps?q={lat},{lon}"
#         print("🌍 Opening location:", maps_url)

#         try:
#             webbrowser.open(maps_url)
#         except:
#             print("⚠️ Could not open browser")

#     return jsonify({"status": "SOS received"}), 200


# # =========================
# # 📡 WEBSOCKET CONNECTION
# # =========================
# @socketio.on('connect')
# def on_connect():
#     print("✅ Client connected for streaming")


# @socketio.on('disconnect')
# def on_disconnect():
#     print("❌ Client disconnected")


# # =========================
# # 📸 CAMERA STREAM (REAL-TIME)
# # =========================
# @socketio.on('message')
# def handle_video(message):
#     try:
#         # Convert message to dict
#         if isinstance(message, str):
#             data = json.loads(message)
#         else:
#             data = message

#         if data.get("type") == "video":
#             image_data = data.get("image")

#             # Decode base64 image
#             img_bytes = base64.b64decode(image_data)
#             np_arr = np.frombuffer(img_bytes, np.uint8)
#             frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#             if frame is None:
#                 print("❌ Frame decode failed")
#                 return

#             # 🔥 Show live video
#             cv2.imshow("📡 LIVE CAMERA STREAM", frame)
#             cv2.waitKey(1)

#     except Exception as e:
#         print("❌ Video Error:", e)


# # =========================
# # 🚨 OPTIONAL: SOS VIA SOCKET
# # =========================
# @socketio.on('sos')
# def handle_socket_sos(data):
#     print("\n🚨 SOS (WebSocket) RECEIVED")
#     print(data)

#     lat = data.get("latitude")
#     lon = data.get("longitude")

#     if lat and lon:
#         url = f"https://www.google.com/maps?q={lat},{lon}"
#         print("🌍 Opening:", url)
#         webbrowser.open(url)


# # =========================
# # 🟢 RUN SERVER
# # =========================
# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5000, debug=True)