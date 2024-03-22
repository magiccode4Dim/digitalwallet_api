from simple_websocket_server import WebSocketServer, WebSocket


import os
SERVER = os.getenv('HOST_OTP_SERVER')
PORT = os.getenv('PORT_OTP_SERVER')
#The server
class MyOtpServer(WebSocket):
    def handle(self):
        for client in clients:
            if client != self:
                #para ser um chat basta no conteudo da mensagem , adicionar as informacoes de quem enviou a mensagme
                client.send_message(self.data)

    def connected(self):
        print(self.address, 'connected')
        for client in clients:
            client.send_message(self.address[0] + u' - connected')
        clients.append(self)
        
    def handle_close(self):
        print(self.address, 'closed')
        for client in clients:
            client.send_message(self.address[0] + u' - disconnected')
        clients.remove(self)


clients = []

#inseguro
server = WebSocketServer(SERVER, PORT,  MyOtpServer)
server.serve_forever()

