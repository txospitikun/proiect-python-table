import pygame
import random
import time  

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

        self.white_off_count = 0
        self.black_off_count = 0

        self.bearing_off_coords = {
            "white": (-550, 0),
            "black": (550, 0)
        }

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

        self.winner = None

        self.vs_ai = False

    def calculate_point_positions(self):
        board_left = 100
        board_top = 50
        board_w = self.width - 200
        board_h = self.height - 200

        gap = board_w 
        half_gap = gap 

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

        self.bar_position = (self.width 

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

        white_off_text = self.font.render(f"White Off: {self.white_off_count}", True, (255, 255, 255))
        black_off_text = self.font.render(f"Black Off: {self.black_off_count}", True, (0, 0, 0))
        self.screen.blit(white_off_text, (10, 40))
        self.screen.blit(black_off_text, (10, 70))

        if self.winner:
            winner_text = self.font.render(f"Winner: {self.winner.capitalize()}", True, (255, 0, 0))
            self.screen.blit(winner_text, (10, 100))

    def draw_backgammon_table(self):
        self.screen.fill(self.background_color)
        board_color = (185, 122, 87)
        pygame.draw.rect(
            self.screen, 
            board_color, 
            (100, 50, self.width - 200, self.height - 200)
        )

        light_brown = (222, 184, 135)
        dark_brown = (139, 69, 19)
        num_points = 12
        board_width = self.width - 200
        board_height = self.height - 200
        point_width = board_width 

        for i in range(num_points):
            color = light_brown if i % 2 == 1 else dark_brown
            offset = 1 if i >= 6 else 0
            tip_x = 100 + (i + offset) * point_width + point_width 
            tip_y = 50 + board_height 
            base_left_x = 100 + (i + offset) * point_width
            base_left_y = 50
            base_right_x = base_left_x + point_width
            base_right_y = base_left_y
            pygame.draw.polygon(
                self.screen, 
                color, 
                [(tip_x, tip_y), (base_left_x, base_left_y), (base_right_x, base_right_y)]
            )

        for i in range(num_points):
            color = light_brown if i % 2 == 0 else dark_brown
            offset = 1 if i >= 6 else 0
            tip_x = 100 + (i + offset) * point_width + point_width 
            tip_y = 50 + board_height 
            base_left_x = 100 + (i + offset) * point_width
            base_left_y = 50 + board_height
            base_right_x = base_left_x + point_width
            base_right_y = base_left_y
            pygame.draw.polygon(
                self.screen, 
                color, 
                [(tip_x, tip_y), (base_left_x, base_left_y), (base_right_x, base_right_y)]
            )

        self.draw_buttons()

        if self.game_started:
            self.draw_pieces()
            self.draw_possible_moves()
            self.draw_bar()
            if self.winner:
                winner_text = self.font.render(f"{self.winner.upper()} WINS!", True, (255, 0, 0))
                self.screen.blit(winner_text, (self.width

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
                color = (255, 255, 0, 130)
                pygame.draw.circle(s, color, (cx, cy), radius)
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
            print("Play with AI clicked.")
            self.start_game_for_ai()  
        elif self.buttons["friend"].collidepoint(pos):
            self.start_game_for_friends()
        elif self.buttons["dice"].collidepoint(pos):
            if self.game_started and not self.winner:
                self.roll_and_assign_dice()
        else:
            if not self.game_started or self.winner:
                return
            if self.bar[self.current_player] > 0:
                self.try_reenter_from_bar(pos)
            else:
                self.attempt_select_or_move(pos)

    def start_game_for_friends(self):
        self.vs_ai = False  
        self._common_game_setup()

    def start_game_for_ai(self):
        self.vs_ai = True
        self._common_game_setup()

    def _common_game_setup(self):
        self.current_player_thrown_dice = False
        self.game_started = False
        self.board = {i: [] for i in range(1, 25)}
        self.bar = {"white": 0, "black": 0}
        self.selected_piece = None
        self.possible_moves.clear()
        self.current_dice.clear()
        self.dice_result = ""
        self.winner = None
        self.white_off_count = 0
        self.black_off_count = 0

        self.board[1]  = [("black", False, False) for _ in range(2)]
        self.board[6]  = [("white", False, False) for _ in range(5)]
        self.board[8]  = [("white", False, False) for _ in range(3)]
        self.board[12] = [("black", False, False) for _ in range(5)]
        self.board[13] = [("white", False, False) for _ in range(5)]
        self.board[17] = [("black", False, False) for _ in range(3)]

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
        else:
            self.current_player = "black"
            self.dice_result += " | Black starts!"

        self.game_started = True

    def roll_dice_once(self):
        return (random.randint(1, 6), random.randint(1, 6))

    def roll_and_assign_dice(self):
        if not self.current_player_thrown_dice:
            d1, d2 = self.roll_dice_once()
            self.current_dice = [d1, d2]
            if d1 == d2:
                self.current_dice.extend([d1, d2])  
            self.dice_result = f"{self.current_player.capitalize()}'s turn: dice {self.current_dice}"
            self.selected_piece = None
            self.possible_moves.clear()
            self.current_player_thrown_dice = True
            self.check_if_has_moves()

    def ai_move(self):
        if not self.current_player_thrown_dice:
            self.roll_and_assign_dice()
            time.sleep(0.5)

        moves_made = 0  
        valid_moves_all = self.collect_all_valid_moves("black")

        while self.current_dice and self.current_player == "black" and not self.winner and self.game_started:
            if moves_made >= 1:  
                self.end_turn()
                break

            if self.bar["black"] > 0:
                if not self.can_reenter_somewhere_for_ai():

                    self.end_turn()
                    return
                else:

                    reentry_done = self.ai_random_reentry()
                    time.sleep(0.5)
                    if reentry_done:
                        moves_made += 1
                    else:
                        self.end_turn()
                        return

            else:

                if not valid_moves_all:

                    self.end_turn()
                    return

                move = random.choice(valid_moves_all)
                spoint, sindex, dest_point = move
                self.execute_move(spoint, sindex, dest_point)
                moves_made += 1
                time.sleep(0.5)

        if not self.current_dice or moves_made >= 2:
            self.end_turn()

    def can_reenter_somewhere_for_ai(self):
        if not self.current_dice:
            return False

        possible_points = [d for d in self.current_dice if 1 <= d <= 6]
        for pt in possible_points:
            if self.can_land_on(pt, "black"):
                return True
        return False

    def ai_random_reentry(self):
        if not self.current_dice:
            return False
        possible_moves = []
        for d in self.current_dice:
            if 1 <= d <= 6:
                pt = d
                if self.can_land_on(pt, "black"):
                    possible_moves.append(pt)
        if not possible_moves:
            return False
        chosen_pt = random.choice(possible_moves)

        self.bar["black"] -= 1
        if self.board[chosen_pt] and len(self.board[chosen_pt]) == 1 and self.board[chosen_pt][0][0] == "white":

            self.board[chosen_pt].clear()
            self.bar["white"] += 1

        self.board[chosen_pt].append(("black", False, False))
        if chosen_pt in self.current_dice:
            self.current_dice.remove(chosen_pt)
        else:

            if self.current_dice:
                self.current_dice.pop(0)
        return True

    def collect_all_valid_moves(self, player_color):
        moves = []

        for i in range(1, 25):
            stack = self.board[i]
            if stack:

                for index_in_stack, piece in enumerate(stack):
                    if piece[0] == player_color:

                        possible = self.calculate_possible_moves_for_piece(i, index_in_stack)
                        moves.extend(possible)
        return moves

    def can_reenter_somewhere(self):
        if not self.current_dice:
            return False

        if self.current_player == "white":
            possible_points = [25 - d for d in self.current_dice if 19 <= 25 - d <= 24]
        else:
            possible_points = [d for d in self.current_dice if 1 <= d <= 6]

        for pt in possible_points:
            if self.can_land_on(pt, self.current_player):
                return True
        return False

    def try_reenter_from_bar(self, pos):
        if not self.current_dice:
            return
        candidate_point = self.find_nearest_point(pos)
        if not candidate_point:
            return
        if self.current_player == "white":
            valid_positions = [25 - d for d in self.current_dice if 19 <= 25 - d <= 24]
            if candidate_point not in valid_positions:
                return

        if self.current_player == "black":
            valid_positions = [d for d in self.current_dice if 1 <= d <= 6]
            if candidate_point not in valid_positions:
                return

        if not self.can_land_on(candidate_point, self.current_player):
            return

        self.bar[self.current_player] -= 1
        if self.board[candidate_point] and len(self.board[candidate_point]) == 1 and self.board[candidate_point][0][0] != self.current_player:
            self.board[candidate_point].clear()
            if self.current_player == "white":
                self.bar["black"] += 1
            else:
                self.bar["white"] += 1

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
        else:
            self.check_if_has_moves()

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
            if start_pt == spoint and p_idx == sindex:
                if dest_pt == -1:
                    return -1
                else:
                    radius = 15
                    cx, cy = self.point_coords[dest_pt]
                    stack_size = len(self.board[dest_pt])
                    if dest_pt <= 12:
                        cy = cy + stack_size * self.stack_offset + radius
                    else:
                        cy = cy - stack_size * self.stack_offset - radius
                    dx = pos[0] - cx
                    dy = pos[1] - cy
                    if dx * dx + dy * dy <= radius * radius:
                        return dest_pt
        return None

    def check_if_has_moves(self):
        if self.bar[self.current_player] > 0:
            if not self.can_reenter_somewhere():
                self.end_turn()
            return

        for i in range(1, 25):
            stack = self.board[i]
            if stack:
                piece_color, _, _ = stack[0]
                if piece_color == self.current_player:
                    for idx in range(len(stack)):
                        moves_for_piece = self.calculate_possible_moves_for_piece(i, idx)
                        if moves_for_piece:
                            return

        if self.is_bearing_mode(self.current_player) and self.can_bear_off_piece(self.current_player):
            return

        self.end_turn()

    def can_bear_off_piece(self, player):
        if not self.is_bearing_mode(player):
            return False

        if player == "white":
            home_points = range(19, 25)
            direction = 25
        else:
            home_points = range(1, 7)
            direction = 0

        for point in home_points:
            if point in self.board and self.board[point]:
                used_dist = abs(direction - point)
                if used_dist in self.current_dice:
                    return True
                if any(die > used_dist for die in self.current_dice):
                    can_remove_with_larger_die = True
                    if player == "white":
                        for p in range(19, point):
                            if p in self.board and any(x[0] == "white" for x in self.board[p]):
                                can_remove_with_larger_die = False
                                break
                    else:
                        for p in range(point+1, 7):
                            if p in self.board and any(x[0] == "black" for x in self.board[p]):
                                can_remove_with_larger_die = False
                                break
                    if can_remove_with_larger_die:
                        return True
        return False

    def is_bearing_mode(self, player):
        if player == "white":
            for i in range(1, 19):
                if i in self.board and self.board[i]:
                    for piece in self.board[i]:
                        if piece[0] == "white":
                            return False
        else:
            for i in range(7, 25):
                if i in self.board and self.board[i]:
                    for piece in self.board[i]:
                        if piece[0] == "black":
                            return False
        return True

    def calculate_possible_moves(self):
        self.current_player_can_win = self.check_near_victory(self.current_player)
        self.possible_moves.clear()
        if not self.selected_piece or not self.current_dice:
            return
        spoint, sindex = self.selected_piece
        piece_color, hov, sel = self.board[spoint][sindex]
        for d in sorted(self.current_dice, reverse=True):
            if piece_color == "white":
                dest = spoint - d
                if dest < 1:
                    if self.all_white_in_home(spoint):
                        self.possible_moves.append((spoint, sindex, -1))
                else:
                    if self.can_land_on(dest, "white"):
                        self.possible_moves.append((spoint, sindex, dest))
            else:
                dest = spoint + d
                if dest > 24:
                    if self.all_black_in_home(spoint):
                        self.possible_moves.append((spoint, sindex, -1))
                else:
                    if self.can_land_on(dest, "black"):
                        self.possible_moves.append((spoint, sindex, dest))

    def calculate_possible_moves_for_piece(self, spoint, sindex):
        possible_moves = []
        piece_color, hov, sel = self.board[spoint][sindex]
        if not self.current_dice:
            return possible_moves
        print(self.current_dice)
        for d in sorted(self.current_dice, reverse=True):
            if piece_color == "white":
                dest = spoint - d
                if dest < 1:
                    if self.all_white_in_home(spoint):
                        possible_moves.append((spoint, sindex, -1))
                else:
                    if self.can_land_on(dest, piece_color):
                        possible_moves.append((spoint, sindex, dest))
            else:
                dest = spoint + d
                if dest > 24:
                    if self.all_black_in_home(spoint):
                        possible_moves.append((spoint, sindex, -1))
                else:
                    if self.can_land_on(dest, piece_color):
                        possible_moves.append((spoint, sindex, dest))

        return possible_moves

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
            if piece_color == "white":
                self.white_off_count += 1
            else:
                self.black_off_count += 1

            self.selected_piece = None
            self.possible_moves.clear()
            used_dist = self.get_used_dist_for_bearing_off(piece_color, spoint)
            if used_dist in self.current_dice:
                self.current_dice.remove(used_dist)
            else:
                if self.current_dice:
                    self.current_dice.pop(0)

            self.check_for_winner()
            if not self.current_dice and not self.winner:
                self.end_turn()
            else:
                if not self.winner:
                    self.check_if_has_moves()
            return

        if len(self.board[dest_point]) == 1:
            other_color, ohov, osel = self.board[dest_point][0]
            if other_color != piece_color:
                self.board[dest_point].clear()
                self.bar[other_color] += 1

        self.board[dest_point].append((piece_color, False, False))
        self.selected_piece = None
        self.possible_moves.clear()

        used_dist = abs(dest_point - spoint)
        if used_dist in self.current_dice:
            self.current_dice.remove(used_dist)
        else:
            if self.current_dice:
                self.current_dice.pop(0)

        self.current_player_can_win = self.check_near_victory(piece_color)
        self.check_for_winner()
        if self.winner:
            return
        if not self.current_dice:
            self.end_turn()
        else:
            self.check_if_has_moves()

    def get_used_dist_for_bearing_off(self, piece_color, spoint):
        if piece_color == "white":
            return spoint
        else:
            return 25 - spoint

    def check_for_winner(self):
        if self.white_off_count >= 15:
            self.winner = "white"
        elif self.black_off_count >= 15:
            self.winner = "black"

    def check_near_victory(self, piece_color):
        if self.bar[piece_color] > 0:
            return False
        if piece_color == "white":
            for pt in range(1, 19):
                for p in self.board[pt]:
                    if p[0] == "white":
                        return False
        else:
            for pt in range(7, 25):
                for p in self.board[pt]:
                    if p[0] == "black":
                        return False
        return True

    def all_white_in_home(self, spoint):
        for pt in range(7, 25):
            for p in self.board[pt]:
                if p[0] == "white":
                    return False
        return True

    def all_black_in_home(self, spoint):
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

        if not self.winner:
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

            if self.vs_ai and self.current_player == "black" and not self.winner and self.game_started:
                self.ai_move()

            self.draw_backgammon_table()
            self.clock.tick(60)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game_gui = GUI(1200, 800, "Backgammon")
    game_gui.gui_loop()