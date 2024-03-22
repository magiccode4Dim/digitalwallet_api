from websocket import create_connection
import os
SERVER = os.getenv('HOST_OTP_SERVER')
PORT = os.getenv('PORT_OTP_SERVER')

MY_OTP_SERVER_URI = f"ws://{SERVER}:{PORT}"

def send_messages(message):
    ws = create_connection(MY_OTP_SERVER_URI)
    ws.send(message)
    ws.close()
