# server.py
import socket
import asyncio
import signal
import sys
import json
import random

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
        self.game_state = None
        self.dice_rolls = (0, 0)

    async def accept_clients(self):
        while True:
            conn, address = await asyncio.get_event_loop().sock_accept(self.server_socket)
            self.clients.append(conn)
            print(f"Connection from: {address}")
            if len(self.clients) == 2:
                await self.initialize_game()
            asyncio.create_task(self.listen_to_client(conn))

    async def listen_to_client(self, conn):
        while True:
            try:
                data = await asyncio.get_event_loop().sock_recv(conn, 1024)
                if not data:
                    break
                message = data.decode()
                print(f"Received: {message}")
                await self.handle_message(message, conn)
            except ConnectionResetError:
                break
        await self.close_connection(conn)

    async def handle_message(self, message, conn):
        try:
            data = json.loads(message)
            if data.get("type") == "roll_dice":
                self.roll_dice()
                await self.broadcast_game_state()
        except Exception as e:
            print(f"Error handling message: {e}")

    def roll_dice(self):
        self.dice_rolls = (random.randint(1, 6), random.randint(1, 6))
        print(f"Dice rolled: {self.dice_rolls}")

    async def broadcast_game_state(self):
        if self.game_state is None:
            self.game_state = self.initialize_board()
        
        message = json.dumps({
            "type": "update",
            "state": self.game_state,
            "dice": self.dice_rolls
        })
        for client in self.clients:
            try:
                await asyncio.get_event_loop().sock_sendall(client, message.encode())
            except Exception as e:
                print(f"Failed to send message: {e}")


    async def initialize_game(self):
        print("Starting game!")
        self.game_state = self.initialize_board()
        self.roll_dice()
        await self.broadcast_game_state()

    @staticmethod
    def initialize_board():
        return {
            0: ("Black", 2),
            5: ("White", 5),
            7: ("White", 3),
            11: ("Black", 5),
            12: ("White", 2),
            17: ("Black", 5),
            19: ("Black", 3),
            23: ("White", 5),
        }

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
