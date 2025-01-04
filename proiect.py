import math
import random
from tkinter import *

player_round = 1
game_finished = False

first_player_choosen = False

table_model = {}

def init_table():
    table_model[0] = ("Black", 2)
    table_model[1] = ("N/A", 0)
    table_model[2] = ("N/A", 0)
    table_model[3] = ("N/A", 0)
    table_model[4] = ("N/A", 0)
    table_model[5] = ("White", 5)
    table_model[6] = ("N/A", 0)
    table_model[7] = ("White", 3)
    table_model[8] = ("N/A", 0)
    table_model[9] = ("N/A", 0)
    table_model[10] = ("N/A", 0)
    table_model[11] = ("Black", 5)
    table_model[12] = ("White", 2)
    table_model[13] = ("N/A", 0)
    table_model[14] = ("N/A", 0)
    table_model[15] = ("N/A", 0)
    table_model[16] = ("N/A", 0)
    table_model[17] = ("Black", 5)
    table_model[18] = ("N/A", 0)
    table_model[19] = ("Black", 3)
    table_model[20] = ("N/A", 0)
    table_model[21] = ("N/A", 0)
    table_model[22] = ("N/A", 0)
    table_model[23] = ("White", 5)

    print("Tabla de joc a fost inițializată!")

def choose_first_player():
    dice1_player1 = math.ceil(6 * random.random())
    dice2_player1 = math.ceil(6 * random.random())

    dice1_player2 = math.ceil(6 * random.random())
    dice2_player2 = math.ceil(6 * random.random())

    print(f"Jucătorul 1 a aruncat zarurile: {dice1_player1} și {dice2_player1}")
    print(f"Jucătorul 2 a aruncat zarurile: {dice1_player2} și {dice2_player2}")
     
    if dice1_player1 + dice2_player1 > dice1_player2 + dice2_player2:
        print("Jucătorul 1 începe jocul!")
        return 1
    else:
        print("Jucătorul 2 începe jocul!")
        return 2

class gui():
    def __init__(self, width, height, offset=25):
        self.root = Tk()
        self.offset_x = width // 11
        print(self.offset_x)
        self.width = width
        self.height = height
        self.label = Label(self.root, text="Joc de table")
        self.button = Button(self.root, text="Aruncă zarurile pentru alegerea primului jucător!", width=30, command=self.roll_dice)
        self.dice_result_label1 = Label(self.root, text="Zarurile nu au fost aruncate încă")
        self.dice_result_label2 = Label(self.root, text="")
        self.canvas = Canvas(self.root, width=self.width, height=self.height)

        self.label.pack()
        self.button.pack()
        self.dice_result_label1.pack()
        self.dice_result_label2.pack()
        self.canvas.pack()
        
        self.draw_table()
        self.root.mainloop()

    def roll_dice(self):
        if first_player_choosen == False:
            dice1_player1 = math.ceil(6 * random.random())
            dice2_player1 = math.ceil(6 * random.random())

            dice1_player2 = math.ceil(6 * random.random())
            dice2_player2 = math.ceil(6 * random.random())

            result_text1 = f"Zarurile aruncate sunt de jucătorul 1 sunt: {dice1_player1} și {dice2_player1}"
            result_text2 = f"\nZarurile aruncate sunt de jucătorul 2 sunt: {dice1_player2} și {dice2_player2}"
            self.dice_result_label.config(text=result_text1)
            self.dice_result_label2.config(text=result_text2)

    def draw_table(self):
        self.canvas.create_rectangle(self.offset_x, self.offset_x, self.width-self.offset_x, self.height-self.offset_x, fill="green")

        piece_diameter = 40
        vertical_gap = 0
        horizontal_gap = 31

        for i in range(24):
            if table_model[i][0] == "Black":
                color = "black"
            elif table_model[i][0] == "White":
                color = "white"
            else:
                color = "green"

            if i < 12:
                for j in range(table_model[i][1]):
                    x0 = self.offset_x + (piece_diameter + horizontal_gap) * i
                    y0 = self.offset_x + (piece_diameter + vertical_gap) * j
                    x1 = x0 + piece_diameter
                    y1 = y0 + piece_diameter
                    oval = self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags="piece")
                    self.canvas.tag_bind(oval, "<Enter>", lambda event, item=oval: self.highlight_piece(item))
                    self.canvas.tag_bind(oval, "<Leave>", lambda event, item=oval: self.unhighlight_piece(item))
            else:
                for j in range(table_model[i][1]):
                    x0 = self.offset_x + (piece_diameter + horizontal_gap) * (i - 12)
                    y0 = 110 + 600 - (piece_diameter + vertical_gap) * (j + 1)
                    x1 = x0 + piece_diameter
                    y1 = y0 + piece_diameter
                    oval = self.canvas.create_oval(x0, y0, x1, y1, fill=color, tags="piece")
                    self.canvas.tag_bind(oval, "<Enter>", lambda event, item=oval: self.highlight_piece(item))
                    self.canvas.tag_bind(oval, "<Leave>", lambda event, item=oval: self.unhighlight_piece(item))

        self.root.update()

    def highlight_piece(self, item):
        self.canvas.itemconfig(item, outline="yellow", width=3)

    def unhighlight_piece(self, item):
        self.canvas.itemconfig(item, outline="white", width=0)
    
def main():
    init_table()
    
    app_gui = gui(1000, 800)

    print("Bine ați venit la table!")

    print("Aruncați zarurile pentru a începe jocul.")

    player_round = choose_first_player()


    while not game_finished:
        if player_round % 2 == 0:
            print("Este rândul jucătorului 1.")
        else:
            print("Este rândul jucătorului 2.")

        input("Apasă Enter pentru a arunca zarurile...")

        dice1 = math.ceil(6 * random.random())
        dice2 = math.ceil(6 * random.random())

        print(f"Zarurile aruncate sunt: {dice1} și {dice2}") 

if __name__ == "__main__":
    main()
