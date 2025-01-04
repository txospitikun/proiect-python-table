import socket
import asyncio
import signal
import sys

class ClientInstance:
    def __init__(self):
        self.host = "127.0.0.1"   
        self.port = 5100
        self.client_socket = socket.socket()
        self.client_socket.setblocking(False)  

    async def connect_to_server(self):
        try:
            await asyncio.get_event_loop().sock_connect(self.client_socket, (self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)

    async def send_message(self, message):
        try:
            await asyncio.get_event_loop().sock_sendall(self.client_socket, message.encode())
        except Exception as e:
            print(f"Failed to send message: {e}")

    async def receive_message(self):
        try:
            return await asyncio.get_event_loop().sock_recv(self.client_socket, 1024)
        except Exception as e:
            print(f"Failed to receive message: {e}")
            return b""

    async def listen_to_server(self):
        while True:
            try:
                data = await self.receive_message()
                if not data:
                    break
                print(f"Received from server: {data.decode()}")
            except ConnectionResetError:
                print("Server disconnected.")
                break

    async def send_messages(self):
        while True:
            message = input(" -> ")
            if message.lower() == "exit":
                break
            await self.send_message(message)

    async def close_connection(self):
        print("Closing connection...")
        self.client_socket.close()

async def main():
    client = ClientInstance()
    await client.connect_to_server()
    try:
        await asyncio.gather(client.listen_to_server(), client.send_messages())
    except asyncio.CancelledError:
        print("Client tasks cancelled.")
    finally:
        await client.close_connection()

def signal_handler(sig, frame):
    print("Caught signal, shutting down client...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
