import pygame
import random


def color_map(col):
    if col == "white":
        return (255, 255, 255)
    elif col == "black":
        return (0, 0, 0)
    return (128, 128, 128)

class GUI:
    def __init__(self, width, height, caption, background_color=(128, 128, 128)):
        pygame.init()
        self.width = width
        self.height = height
        self.stack_offset = 30
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        self.background_color = background_color
        self.screen.fill(self.background_color)
        self.player1_score = 0
        pygame.display.flip()

        self.font = pygame.font.SysFont(None, 30)
        self.buttons = {
            "ai": pygame.Rect(50, 10, 130, 30),
            "friend": pygame.Rect(190, 10, 170, 30),
            "dice": pygame.Rect(370, 10, 120, 30),
        }
        self.dice_result = ""

        self.board = {i: [] for i in range(1, 25)}
        self.game_started = False
        self.current_player = None
        self.current_player_thrown_dice = False
        self.current_dice = []
        self.current_player_can_win = False
        self.possible_moves = []
        self.selected_piece = None

        self.bar = {"white": 0, "black": 0}

        self.point_coords = {}
        self.calculate_point_positions()

    def calculate_point_positions(self):
        board_left = 100
        board_top = 50
        board_w = self.width - 200
        board_h = self.height - 200

        gap = board_w // (12 + 1)  
        half_gap = gap // 2

        for i in range(12):
            offset = 1 if i >= 6 else 0
            point_index = 12 - i
            center_x = board_left + (i + offset) * gap + half_gap
            center_y = board_top + 10
            self.point_coords[point_index] = (center_x, center_y)

        for i in range(12):
            offset = 1 if i >= 6 else 0
            point_index = 13 + i
            center_x = board_left + (i + offset) * gap + half_gap
            center_y = board_top + board_h - 10
            self.point_coords[point_index] = (center_x, center_y)

        self.bar_position = (self.width // 2, self.height // 2)

    def draw_buttons(self):
        pygame.draw.rect(self.screen, (200, 200, 200), self.buttons["ai"])
        pygame.draw.rect(self.screen, (200, 200, 200), self.buttons["friend"])
        pygame.draw.rect(self.screen, (200, 200, 200), self.buttons["dice"])

        ai_text = self.font.render("Play with AI", True, (0, 0, 0))
        friend_text = self.font.render("Play with Friend", True, (0, 0, 0))
        dice_text = self.font.render("Throw Dice", True, (0, 0, 0))
        result_text = self.font.render(self.dice_result, True, (0, 0, 0))

        self.screen.blit(ai_text, (self.buttons["ai"].x + 5, self.buttons["ai"].y + 5))
        self.screen.blit(friend_text, (self.buttons["friend"].x + 5, self.buttons["friend"].y + 5))
        self.screen.blit(dice_text, (self.buttons["dice"].x + 5, self.buttons["dice"].y + 5))
        self.screen.blit(result_text, (520, 15))

    def draw_backgammon_table(self):
        self.screen.fill(self.background_color)
        board_color = (185, 122, 87)
        pygame.draw.rect(self.screen, board_color, (100, 50, self.width - 200, self.height - 200))

        light_brown = (222, 184, 135)
        dark_brown = (139, 69, 19)
        num_points = 12
        board_width = self.width - 200
        board_height = self.height - 200
        point_width = board_width // (num_points + 1)

        for i in range(num_points):
            color = light_brown if i % 2 == 0 else dark_brown
            offset = 1 if i >= 6 else 0
            tip_x = 100 + (i + offset) * point_width + point_width // 2
            tip_y = 50 + board_height // 2
            base_left_x = 100 + (i + offset) * point_width
            base_left_y = 50
            base_right_x = base_left_x + point_width
            base_right_y = base_left_y
            pygame.draw.polygon(
                self.screen, color,
                [(tip_x, tip_y), (base_left_x, base_left_y), (base_right_x, base_right_y)]
            )

        for i in range(num_points):
            color = light_brown if i % 2 == 0 else dark_brown
            offset = 1 if i >= 6 else 0
            tip_x = 100 + (i + offset) * point_width + point_width // 2
            tip_y = 50 + board_height // 2
            base_left_x = 100 + (i + offset) * point_width
            base_left_y = 50 + board_height
            base_right_x = base_left_x + point_width
            base_right_y = base_left_y
            pygame.draw.polygon(
                self.screen, color,
                [(tip_x, tip_y), (base_left_x, base_left_y), (base_right_x, base_right_y)]
            )

        self.draw_buttons()
        if self.game_started:
            self.draw_pieces()
            self.draw_possible_moves()
            self.draw_bar()

    def draw_pieces(self):
        radius = 15
        for point_idx, stack in self.board.items():
            cx, cy = self.point_coords[point_idx]
            if point_idx <= 12:
                for i, piece in enumerate(stack):
                    color, hovered, selected = piece
                    px = cx
                    py = cy + i*self.stack_offset + radius
                    outline = (255, 255, 0) if ((hovered or selected) and self.current_player in color) else (0, 0, 0)
                    pygame.draw.circle(self.screen, color_map(color), (px, py), radius)
                    pygame.draw.circle(self.screen, outline, (px, py), radius, 2)
            else:
                for i, piece in enumerate(stack):
                    color, hovered, selected = piece
                    px = cx
                    py = cy - i*self.stack_offset - radius
                    outline = (255, 255, 0) if ((hovered or selected) and self.current_player in color) else (0, 0, 0)
                    pygame.draw.circle(self.screen, color_map(color), (px, py), radius)
                    pygame.draw.circle(self.screen, outline, (px, py), radius, 2)


    def draw_bar(self):
        bar_x, bar_y = self.bar_position
        radius = 15

        for i in range(self.bar["white"]):
            pygame.draw.circle(self.screen, color_map("white"), (bar_x - 50, bar_y - i * self.stack_offset), radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (bar_x - 50, bar_y - i * self.stack_offset), radius, 2)

        for i in range(self.bar["black"]):
            pygame.draw.circle(self.screen, color_map("black"), (bar_x + 50, bar_y - i * self.stack_offset), radius)
            pygame.draw.circle(self.screen, (0, 0, 0), (bar_x + 50, bar_y - i * self.stack_offset), radius, 2)

    def draw_possible_moves(self):
        if not self.possible_moves:
            return
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        radius = 15
        for (start_point, piece_index, dest_point) in self.possible_moves:
            if dest_point == -1:
                cx, cy = self.bar_position
                cx += 550 if self.current_player == "white" else -550
                stack_size = self.bar[self.current_player]
                py = cy - stack_size * self.stack_offset - radius
                color = (255, 255, 0, 130)
                pygame.draw.circle(s, color, (cx, py), radius)
            else:
                cx, cy = self.point_coords[dest_point]
                stack_size = len(self.board[dest_point])
                if dest_point <= 12:
                    py = cy + stack_size * self.stack_offset + radius
                else:
                    py = cy - stack_size * self.stack_offset - radius
                color = (255, 255, 0, 130)
                pygame.draw.circle(s, color, (cx, py), radius)
        self.screen.blit(s, (0, 0))

    def handle_click(self, pos):
        if self.buttons["ai"].collidepoint(pos):
            print("Play with AI clicked. AI not yet implemented.")
        elif self.buttons["friend"].collidepoint(pos):
            self.start_game_for_friends()
        elif self.buttons["dice"].collidepoint(pos):
            if self.game_started:
                self.roll_and_assign_dice()
        else:
            if not self.game_started:
                return
            if self.bar[self.current_player] > 0:
                self.try_reenter_from_bar(pos)
            else:
                self.attempt_select_or_move(pos)

    def start_game_for_friends(self):
        self.current_player_thrown_dice = False
        self.game_started = False
        self.board = {i: [] for i in range(1, 25)}
        self.bar = {"white": 0, "black": 0}
        self.selected_piece = None
        self.possible_moves.clear()
        self.current_dice.clear()
        self.dice_result = ""

        self.board[19] = [("black", False, False) for _ in range(5)]
        self.board[12] = [("black", False, False) for _ in range(5)]
        self.board[8]  = [("white", False, False) for _ in range(3)]
        self.board[6]  = [("white", False, False) for _ in range(5)]

        self.board[1]  = [("black", False, False) for _ in range(2)]
        self.board[13] = [("white", False, False) for _ in range(5)]
        self.board[17] = [("black", False, False) for _ in range(3)]
        self.board[24] = [("white", False, False) for _ in range(2)]


        # winning condition
        # all black in the winning area
        # self.board[24] = [("black", False, False) for _ in range(6)]
        # self.board[23] = [("black", False, False) for _ in range(6)]
        # self.board[22] = [("black", False, False) for _ in range(6)]

        
        (w1, w2) = self.roll_dice_once()
        (b1, b2) = self.roll_dice_once()

        
        sum_white = w1 + w2
        sum_black = b1 + b2

        while sum_white == sum_black:
            (w1, w2) = self.roll_dice_once()
            (b1, b2) = self.roll_dice_once()
            sum_white = w1 + w2
            sum_black = b1 + b2
        
        self.dice_result = f"White dice: {w1},{w2} | Black dice: {b1},{b2}"
        if sum_white > sum_black:
            self.current_player = "white"
            self.dice_result += " | White starts!"
        elif sum_white < sum_black:
            self.current_player = "black"
            self.dice_result += " | Black starts!"
        else:
            self.current_player = "white"

        self.game_started = True

    def roll_dice_once(self):
        return (random.randint(1, 6), random.randint(1, 6))

    def roll_and_assign_dice(self):
        if self.current_player_thrown_dice == False:
            self.current_dice = [random.randint(1, 6), random.randint(1, 6)]
            if self.current_dice[0] == self.current_dice[1]:
                self.current_dice.extend(self.current_dice)
            self.dice_result = f"{self.current_player.capitalize()}'s turn: dice {self.current_dice}"
            self.selected_piece = None
            self.possible_moves.clear()
            self.current_player_thrown_dice = True

    def try_reenter_from_bar(self, pos):
        if not self.current_dice:
            return  

        candidate_point = self.find_nearest_point(pos)
        if not candidate_point:
            return

        if self.current_player == "white":
            if candidate_point < 19 or candidate_point > 24:
                return 
        else:  
            if candidate_point < 1 or candidate_point > 6:
                return 

        if not self.can_land_on(candidate_point, self.current_player):
            return

        self.bar[self.current_player] -= 1

        if self.board[candidate_point] and self.board[candidate_point][0][0] != self.current_player:
            other_color, ohov, osel = self.board[candidate_point][0]
            self.board[candidate_point].clear()
            self.bar[other_color] += 1

        self.board[candidate_point].append((self.current_player, False, False))


        if self.current_player == "white":
            used_dist = 25 - candidate_point
        else:
            used_dist = candidate_point

        if used_dist in self.current_dice:
            self.current_dice.remove(used_dist)
        else:
            if self.current_dice:
                self.current_dice.pop(0)

        if not self.current_dice:
            self.end_turn()

    def find_nearest_point(self, pos):
        best_dist = float("inf")
        best_point = None
        mx, my = pos
        for p, (cx, cy) in self.point_coords.items():
            dist = (mx - cx)**2 + (my - cy)**2
            if dist < best_dist:
                best_dist = dist
                best_point = p
        return best_point

    def attempt_select_or_move(self, pos):
        clicked_point, clicked_piece_index = self.find_piece_at(pos)
        if clicked_point:
            piece_color, h, s = self.board[clicked_point][clicked_piece_index]
            if piece_color != self.current_player:
                return  
            if self.selected_piece:
                spoint, sindex = self.selected_piece
                sc, sh, ss = self.board[spoint][sindex]
                self.board[spoint][sindex] = (sc, sh, False)
            self.selected_piece = (clicked_point, clicked_piece_index)
            c, hov, sel = self.board[clicked_point][clicked_piece_index]
            self.board[clicked_point][clicked_piece_index] = (c, hov, True)
            self.calculate_possible_moves()
        else:
            if self.selected_piece:
                spoint, sindex = self.selected_piece
                valid_dest = self.find_move_if_valid(pos, spoint, sindex)
                if valid_dest is not None:
                    self.execute_move(spoint, sindex, valid_dest)

    def find_piece_at(self, pos):
        radius = 15
        mx, my = pos
        for point_idx, stack in self.board.items():
            if point_idx <= 12:
                for i, piece in enumerate(stack):
                    color, hov, sel = piece
                    px, py = self.point_coords[point_idx]
                    py += i * self.stack_offset + radius
                    if (mx - px)**2 + (my - py)**2 <= radius**2:
                        return point_idx, i
            else:
                for i, piece in enumerate(stack):
                    color, hov, sel = piece
                    px, py = self.point_coords[point_idx]
                    py -= i * self.stack_offset + radius
                    if (mx - px)**2 + (my - py)**2 <= radius**2:
                        return point_idx, i
        return (None, None)

    def find_move_if_valid(self, pos, spoint, sindex):
        for (start_pt, p_idx, dest_pt) in self.possible_moves:
            if dest_pt == -1:
                return -1
            else:
                if start_pt == spoint and p_idx == sindex:
                    cx, cy = self.point_coords[dest_pt]
                    stack_size = len(self.board[dest_pt])
                    radius = 15
                    if dest_pt <= 12:
                        cy = cy + stack_size * self.stack_offset + radius
                    else:
                        cy = cy - stack_size * self.stack_offset - radius
                    dx = pos[0] - cx
                    dy = pos[1] - cy
                    if dx * dx + dy * dy <= radius * radius:
                        return dest_pt
        return None

    def calculate_possible_moves(self):
        self.current_player_can_win = self.check_near_victory(self.current_player)
        self.possible_moves.clear()
        if not self.selected_piece or not self.current_dice:
            return
        spoint, sindex = self.selected_piece
        piece_color, hov, sel = self.board[spoint][sindex]
        print(f"Selected piece: {spoint} - {piece_color}")
        if self.current_player_can_win:
            for d in sorted(self.current_dice, reverse=True):
                if piece_color == "white":
                    higher_points = []
                    for pt in range(1, d):
                        for p in self.board[pt]:
                            if p[0] == "white":
                                higher_points.append(pt)
                                break  
                    if spoint in higher_points:
                        self.possible_moves.append((spoint, sindex, -1))
                else:
                    higher_points = []
                    for pt in range(25 - d, 25):
                        for p in self.board[pt]:
                            if p[0] == "black":
                                higher_points.append(pt)
                                break  
                    print(f"Higher points: {higher_points}")
                    if spoint in higher_points:
                        self.possible_moves.append((spoint, sindex, -1))
        else:
            for d in self.current_dice:
                if piece_color == "white":
                    dest = spoint - d  
                else:
                    dest = spoint + d  
                if 1 <= dest <= 24:
                    if self.can_land_on(dest, piece_color):
                        self.possible_moves.append((spoint, sindex, dest))
        print(f"Possible moves: {self.possible_moves}")

    def can_land_on(self, dest_point, piece_color):
        stack = self.board[dest_point]
        if not stack:
            return True
        top_color = stack[0][0]
        if top_color == piece_color:
            return True
        else:
            if len(stack) == 1:
                return True
        return False

    def execute_move(self, spoint, sindex, dest_point):
        piece_color, hov, sel = self.board[spoint][sindex]
        self.board[spoint].pop(sindex)

        if dest_point == -1:
            self.player1_score += 1
            print(self.player1_score)
            self.selected_piece = None
            self.possible_moves.clear()
            if self.current_dice:
                self.current_dice.pop(0)
            if not self.current_dice:
                self.end_turn()
            return

        if len(self.board[dest_point]) == 1:
            other_color, ohov, osel = self.board[dest_point][0]
            if other_color != piece_color:
                self.board[dest_point].clear()
                self.bar[other_color] += 1

        self.board[dest_point].append((piece_color, False, False))
        self.selected_piece = None
        self.possible_moves.clear()

        if piece_color == "white":
            if spoint <= 12:
                used_dist = spoint - dest_point  
            else:
                used_dist = dest_point - spoint 
        else:
            if spoint <= 12:
                used_dist = dest_point - spoint  
            else:
                used_dist = spoint - dest_point 

        if used_dist in self.current_dice:
            self.current_dice.remove(used_dist)
        else:
            if self.current_dice:
                self.current_dice.pop(0)

        if self.check_near_victory(piece_color):
            print(self.current_player_can_win)
            if self.current_player == piece_color:
                self.current_player_can_win = True
            else:
                self.current_player_can_win = False
            return

        if not self.current_dice:
            self.end_turn()

    def check_near_victory(self, piece_color):
        if self.bar[piece_color] > 0:
            return False
        if piece_color == "white":
            for pt in range(7, 25):
                for p in self.board[pt]:
                    if p[0] == "white":
                        return False
        else:
            for pt in range(1, 19):
                for p in self.board[pt]:
                    if p[0] == "black":
                        return False
        return True

    def end_turn(self):
        self.current_player_thrown_dice = False
        if self.current_player == "white":
            self.current_player = "black"
        else:
            self.current_player = "white"
        if self.current_player:
            self.dice_result = f"{self.current_player.capitalize()}'s turn - throw dice!"
        self.selected_piece = None
        self.possible_moves.clear()

    def update_hover_states(self):
        if not self.game_started or not self.current_player or not self.current_player_thrown_dice:
            return
        mx, my = pygame.mouse.get_pos()
        radius = 15
        for point_idx, stack in self.board.items():
            new_stack = []
            for i, (clr, hov, sel) in enumerate(stack):
                px, py = self.point_coords[point_idx]
                if point_idx <= 12:
                    py = py + i * self.stack_offset + radius
                else:
                    py = py - i * self.stack_offset - radius
                dist = (mx - px)**2 + (my - py)**2
                is_hover = (dist <= radius**2) and (clr == self.current_player)
                new_stack.append((clr, is_hover, sel))
            self.board[point_idx] = new_stack

    def gui_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.update_hover_states()
            self.draw_backgammon_table()
            self.clock.tick(60)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game_gui = GUI(1200, 800, "Backgammon")
    game_gui.gui_loop()