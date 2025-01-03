import math
import random

player_round = 0
game_finished = False


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

def main():
    print("Bine ați venit la table!")

    init_table()

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
