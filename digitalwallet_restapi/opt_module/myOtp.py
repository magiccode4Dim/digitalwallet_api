from websocket import create_connection

MY_OTP_SERVER_URI = 'ws://localhost:3001'

def send_messages(message):
    ws = create_connection(MY_OTP_SERVER_URI)
    ws.send(message)
    ws.close()
