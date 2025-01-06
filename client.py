# client.py
import socket
import asyncio
import signal
import sys
import json
from tkinter import *

class ClientInstance:
    def __init__(self):
        self.host = "127.0.0.1" 
        self.port = 5100
        self.client_socket = socket.socket()
        self.client_socket.setblocking(False)  
        self.game_state = None
        self.dice_rolls = (0, 0)
        self.current_player = None
        self.highlighted_piece = None
        self.app = BackgammonGUI(self) 

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
                message = json.loads(data.decode())
                if message.get("type") == "update":
                    self.game_state = message.get("state")
                    self.dice_rolls = message.get("dice", (0, 0))
                    self.current_player = message.get("current_player")
                    self.update_board()
                elif message.get("type") == "start":
                    self.game_state = message.get("state")
                    self.dice_rolls = message.get("dice", (0, 0))
                    self.current_player = message.get("current_player")
                    self.initialize_board()
            except ConnectionResetError:
                print("Server disconnected.")
                break

    async def close_connection(self):
        print("Closing connection...")
        self.client_socket.close()

    def initialize_board(self):
        print("Game started!")
        self.app.update_game_state(self.game_state)
        self.app.update_dice(self.dice_rolls)
        self.app.update_current_player(self.current_player)

    def update_board(self):
        if self.app:
            self.app.update_game_state(self.game_state)
            self.app.update_dice(self.dice_rolls)
            self.app.update_current_player(self.current_player)

class BackgammonGUI:
    def __init__(self, client):
        self.client = client
        self.root = Tk()
        self.root.title("Multiplayer Backgammon")
        self.canvas = Canvas(self.root, width=1100, height=600, bg="green")
        self.canvas.pack()

        # Add labels for scores
        self.score_black = StringVar()
        self.score_white = StringVar()
        self.current_player_label = StringVar()
        self.score_black.set("Black: 0")
        self.score_white.set("White: 0")
        self.current_player_label.set("Current Player: -")

        Label(self.root, textvariable=self.score_black, fg="black", font=("Helvetica", 16)).pack()
        Label(self.root, textvariable=self.score_white, fg="white", bg="black", font=("Helvetica", 16)).pack()
        Label(self.root, textvariable=self.current_player_label, font=("Helvetica", 16)).pack()

        # Add labels for dice
        self.dice_label = StringVar()
        self.dice_label.set("Dice: - , -")
        Label(self.root, textvariable=self.dice_label, font=("Helvetica", 16)).pack()

        # Add button to roll dice
        self.roll_button = Button(self.root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack()

        self.highlighted_piece = None
        self.valid_moves = []

        self.canvas.bind("<Motion>", self.on_hover)
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()
        asyncio.create_task(self.start_main_loop())

    def draw_board(self):
        # Draw board triangles and space for taken pieces
        for i in range(12):
            x0 = 50 + i * 70
            y0 = 50
            x1 = x0 + 35
            y1 = 300
            self.canvas.create_polygon(x0, y0, x1, y1, x0 + 70, y0, fill="brown" if i % 2 == 0 else "beige")

        for i in range(12):
            x0 = 50 + i * 70
            y0 = 600
            x1 = x0 + 35
            y1 = 350
            self.canvas.create_polygon(x0, y0, x1, y1, x0 + 70, y0, fill="brown" if i % 2 == 0 else "beige")

        # Add space for taken pieces in the middle
        self.canvas.create_rectangle(430, 50, 490, 600, fill="darkgreen")

    def update_game_state(self, state):
        self.canvas.delete("pieces")
        for position, (color, count) in state.items():
            position = int(position)
            for i in range(count):
                column = position % 12
                x = 50 + column * 70 + 20
                y = 50 + i * 30 if position < 12 else 550 - i * 30
                self.canvas.create_oval(x, y, x + 30, y + 30, fill=color.lower(), tags="pieces")

    def update_dice(self, dice):
        self.dice_label.set(f"Dice: {dice[0]} , {dice[1]}")

    def update_current_player(self, current_player):
        self.current_player_label.set(f"Current Player: {current_player}")
        if self.client.client_socket.getsockname()[1] != current_player:
            self.roll_button.config(state=DISABLED)
        else:
            self.roll_button.config(state=NORMAL)

    def roll_dice(self):
        message = json.dumps({"type": "roll_dice"})
        asyncio.create_task(self.client.send_message(message))

    def on_hover(self, event):
        self.canvas.delete("highlight")
        item = self.canvas.find_closest(event.x, event.y)
        if "pieces" in self.canvas.gettags(item):
            self.canvas.itemconfig(item, outline="yellow", width=2, tags="highlight")

    def on_click(self, event):
        self.canvas.delete("valid_moves")
        item = self.canvas.find_closest(event.x, event.y)
        if "pieces" in self.canvas.gettags(item):
            self.highlighted_piece = item
            # Calculate valid moves (placeholder)
            self.valid_moves = [(event.x + 70, event.y), (event.x + 140, event.y)]
            for move in self.valid_moves:
                x, y = move
                self.canvas.create_oval(x, y, x + 30, y + 30, fill="lightblue", stipple="gray50", tags="valid_moves")

    async def start_main_loop(self):
        while True:
            self.root.update()
            await asyncio.sleep(0.01)

async def main():
    client = ClientInstance()
    await client.connect_to_server()
    try:
        await client.listen_to_server()
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
