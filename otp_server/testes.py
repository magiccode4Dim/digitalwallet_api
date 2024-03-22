from RSA_encript_and_decript import encrypt_message,decrypt_message


SERVER_PUBLIC_PATH = "KEYS/WEB_SOCKET_SERVER_KEYS/public_key.pem"

message = encrypt_message("ola",SERVER_PUBLIC_PATH)


print("Mensagem encriptada "+str(message))

SERVER_PRIVATE_PATH = "KEYS/WEB_SOCKET_SERVER_KEYS/private_key.pem"


decriptedmessage = decrypt_message(str(message),SERVER_PRIVATE_PATH)


print(decriptedmessage)
