import socket
import asyncio
import signal
import sys

class ServerInstance:
    def __init__(self):
        self.host = "127.0.0.1" 
        self.port = 5100
        self.server_socket = socket.socket()
        self.server_socket.setblocking(False)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        self.clients = []

    async def accept_clients(self):
        while True:
            conn, address = await asyncio.get_event_loop().sock_accept(self.server_socket)
            self.clients.append(conn)
            print(f"Connection from: {address}")
            asyncio.create_task(self.listen_to_client(conn))

    async def listen_to_client(self, conn):
        while True:
            try:
                data = await asyncio.get_event_loop().sock_recv(conn, 1024)
                if not data:
                    break
                print(f"From connected user: {data.decode()}")
                await self.send_message(f"Echo: {data.decode()}", conn)
            except ConnectionResetError:
                break
        await self.close_connection(conn)

    async def send_message(self, message, conn=None):
        if conn:
            try:
                await asyncio.get_event_loop().sock_sendall(conn, message.encode())
            except Exception as e:
                print(f"Failed to send message: {e}")
        else:
            for client in self.clients:
                try:
                    await asyncio.get_event_loop().sock_sendall(client, message.encode())
                except Exception as e:
                    print(f"Failed to send message: {e}")

    async def close_connection(self, conn):
        conn.close()
        if conn in self.clients:
            self.clients.remove(conn)

    async def shutdown(self):
        print("Shutting down server...")
        for client in self.clients:
            await self.close_connection(client)
        self.server_socket.close()

server = ServerInstance()

def signal_handler(sig, frame):
    print("Caught signal, shutting down server...")
    asyncio.run(server.shutdown())
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

async def main():
    try:
        await server.accept_clients()
    except asyncio.CancelledError:
        print("Server stopped.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")
