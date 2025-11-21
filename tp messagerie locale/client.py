import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

class Client:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print(f" Connecté au serveur sur {self.host}:{self.port}")
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True 
            receive_thread.start()
            
            self.send_messages()
            
        except ConnectionRefusedError:
            print(f" ERREUR : Connexion refusée. Assurez-vous que le serveur est démarré sur {self.host}:{self.port}.")
        except Exception as e:
            print(f" ERREUR inattendue lors de la connexion : {e}")
        finally:
            self.client_socket.close()

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                
                if not data:
                    print("\n👋 Déconnecté du serveur.")
                    break
                
                message = data.decode('utf-8')
                
                sys.stdout.write('\r' + ' ' * 50 + '\r') 
                print(message)
                sys.stdout.write("> ") 
                sys.stdout.flush()

            except ConnectionResetError:
                print("\n La connexion a été réinitialisée par le serveur.")
                break
            except Exception as e:
                print(f"\n Erreur lors de la réception : {e}")
                break
        
        self.client_socket.close()
        sys.exit()

    def send_messages(self):
        print("Entrez votre message (tapez 'quitter' pour arrêter) :")
        while True:
            try:
                message = input("> ")
                
                if message.lower() == 'quitter':
                    print("Déconnexion demandée.")
                    break
                
                self.client_socket.send(message.encode('utf-8'))
                
            except EOFError:
                break
            except Exception:
                break
        
        self.client_socket.close()


if __name__ == '__main__':
    chat_client = Client(HOST, PORT)
    chat_client.connect_to_server()