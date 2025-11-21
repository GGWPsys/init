import socket
import threading

# Configuration serveur
HOST = '0.0.0.0'
PORT = 65432

class Serveur:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def broadcast(self, message):
        encoded_message = message.encode('utf-8')
        for client in self.clients:
            try:
                client.sendall(encoded_message)
            except Exception as e:
                print(f"Erreur lors de l'envoi au client: {e}")
                self._remove_client(client)

    def _remove_client(self, client_socket):
        if client_socket in self.clients:
            try:
                client_address = client_socket.getpeername()
                print(f" Suppression de la connexion de {client_address}.")
                self.broadcast(f"Le client {client_address[0]} a quitté le chat.")
            except socket.error:
                print(f" Suppression d'un client déconnecté.")
            
            self.clients.remove(client_socket)
            try:
                client_socket.close()
            except Exception:
                pass

    def handle_client(self, client_socket, client_address):
        print(f" Nouvelle connexion de {client_address}")

        self.clients.append(client_socket)
    
        while True:
            try:
                message_bytes = client_socket.recv(1024)
                
                if not message_bytes:
                    self._remove_client(client_socket)
                    break

                message = message_bytes.decode('utf-8')
                
                if message:
                    print(f"Message reçu de {client_address}: {message}")
                    full_message = f"[{client_address[0]}]: {message}"
                    self.broadcast(full_message)

            except ConnectionResetError:
                print(f" Connexion réinitialisée avec {client_address}")
                self._remove_client(client_socket)
                break
            except Exception as e:
                print(f" Déconnexion de {client_address} (Erreur: {e})")
                self._remove_client(client_socket)
                break

    def start(self):
        server = self.server_socket 
        
        server.bind((self.host, self.port))
    
        server.listen(5)
    
        print(f"🚀 Serveur démarré et écoute sur {self.host}:{self.port}")
    
        while True:
            try:
                client_socket, client_address = server.accept()
            
                #thread pour gérer client
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.start()
            
                print(f"Clients actifs : {threading.active_count() - 1}")
            
            except KeyboardInterrupt:
                server.close()
                break
            except Exception as e:
                print(f"Erreur dans la boucle d'acceptation: {e}")


if __name__ == '__main__':
    chat_server = Serveur(HOST, PORT)
    chat_server.start()