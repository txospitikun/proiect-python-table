import pygame
import random

class GUI:
    def __init__(self, width, height, caption, background_color=(128, 128, 128)):
        pygame.init()
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)
        self.background_color = background_color
        self.screen.fill(self.background_color)
        pygame.display.flip()

        self.font = pygame.font.SysFont(None, 30)
        self.buttons = {
            "ai": pygame.Rect(50, 10, 130, 30),
            "friend": pygame.Rect(190, 10, 170, 30),
            "dice": pygame.Rect(370, 10, 120, 30)
        }
        self.dice_result = ""

        self.board = {i: [] for i in range(1, 25)}
        self.game_started = False
        self.current_player = None
        self.current_dice = []
        self.possible_moves = []

        self.point_coords = {}
        self.selected_piece = None  

        self.calculate_point_positions()

    def calculate_point_positions(self):
        board_left = 50
        board_top = 50
        board_w = self.width - 100
        board_h = self.height - 100

        gap = board_w // (12 + 1) 
        half_h = board_h // 2

        for i in range(12):
            offset = 1 if i >= 6 else 0
            point_index = 12 - i
            center_x = board_left + (i + offset) * gap + gap // 2
            center_y = board_top + 10  # near the top
            self.point_coords[point_index] = (center_x, center_y)

        for i in range(12):
            offset = 1 if i >= 6 else 0
            point_index = 13 + i
            center_x = board_left + (i + offset) * gap + gap // 2
            center_y = board_top + board_h - 10  # near bottom
            self.point_coords[point_index] = (center_x, center_y)

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
        self.screen.blit(result_text, (500, 15))

    def draw_backgammon_table(self):
        self.screen.fill(self.background_color)
        board_color = (185, 122, 87)
        pygame.draw.rect(self.screen, board_color, (50, 50, self.width - 100, self.height - 100))

        light_brown = (222, 184, 135)
        dark_brown = (139, 69, 19)
        num_points = 12
        board_width = self.width - 100
        board_height = self.height - 100
        point_width = board_width // (num_points + 1)
        point_height = board_height // 2

        for i in range(num_points):
            color = light_brown if i % 2 == 0 else dark_brown
            offset = 1 if i >= 6 else 0
            tip_x = 50 + (i + offset) * point_width + point_width // 2
            tip_y = 50 + point_height
            base_left_x = 50 + (i + offset) * point_width
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
            tip_x = 50 + (i + offset) * point_width + point_width // 2
            tip_y = 50 + board_height - point_height
            base_left_x = 50 + (i + offset) * point_width
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

    def draw_pieces(self):
        radius = 15
        stack_offset = 20
        for point_idx, stack in self.board.items():
            center_x, center_y = self.point_coords[point_idx]
            if point_idx <= 12:
                # top row
                for i, piece in enumerate(stack):
                    color, hovered, selected = piece
                    px = center_x
                    py = center_y + i * stack_offset + radius
                    outline = (255, 255, 0) if (hovered or selected) else (0, 0, 0)
                    if self.current_player and (self.current_player in color):
                        pygame.draw.circle(self.screen, color_map(color), (px, py), radius)
                        pygame.draw.circle(self.screen, outline, (px, py), radius, 2)
                    else:
                        pygame.draw.circle(self.screen, color_map(color), (px, py), radius)
                        pygame.draw.circle(self.screen, (0, 0, 0), (px, py), radius, 1)
            else:
                for i, piece in enumerate(stack):
                    color, hovered, selected = piece
                    px = center_x
                    py = center_y - i * stack_offset - radius
                    outline = (255, 255, 0) if (hovered or selected) else (0, 0, 0)
                    if self.current_player and (self.current_player in color):
                        pygame.draw.circle(self.screen, color_map(color), (px, py), radius)
                        pygame.draw.circle(self.screen, outline, (px, py), radius, 2)
                    else:
                        pygame.draw.circle(self.screen, color_map(color), (px, py), radius)
                        pygame.draw.circle(self.screen, (0, 0, 0), (px, py), radius, 1)

    def draw_possible_moves(self):
        s = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Transparent overlay
        radius = 15
        for (start_point, piece_index, dest_point) in self.possible_moves:
            dx, dy = self.point_coords[dest_point]
            stack_size = len(self.board[dest_point])
            if dest_point <= 12:
                py = dy + stack_size * 20 + radius
            else:
                py = dy - stack_size * 20 - radius
            px = dx
            color = (255, 255, 0, 128)
            pygame.draw.circle(s, color, (px, py), radius)
        self.screen.blit(s, (0, 0))

    def handle_click(self, pos):
        if self.buttons["ai"].collidepoint(pos):
            print("Play with AI clicked.")
        elif self.buttons["friend"].collidepoint(pos):
            print("Play with Friend clicked.")
            self.start_game_for_friends()
        elif self.buttons["dice"].collidepoint(pos):
            if self.game_started:
                self.roll_and_assign_dice()
        else:
            if not self.game_started:
                return
            self.attempt_select_or_move(pos)

    def start_game_for_friends(self):
        self.board = {i: [] for i in range(1, 25)}
        self.board[1]  = [("white", False, False) for _ in range(2)]
        self.board[12] = [("white", False, False) for _ in range(5)]
        self.board[17] = [("white", False, False) for _ in range(3)]
        self.board[19] = [("white", False, False) for _ in range(5)]
        self.board[24] = [("black", False, False) for _ in range(2)]
        self.board[13] = [("black", False, False) for _ in range(5)]
        self.board[8]  = [("black", False, False) for _ in range(3)]
        self.board[6]  = [("black", False, False) for _ in range(5)]

        (p1d1, p1d2) = self.roll_dice_once()
        (p2d1, p2d2) = self.roll_dice_once()
        sum1 = p1d1 + p1d2
        sum2 = p2d1 + p2d2
        self.dice_result = f"P1 dice: {p1d1},{p1d2} | P2 dice: {p2d1},{p2d2}"
        if sum1 > sum2:
            self.current_player = "white"
        else:
            self.current_player = "black"

        self.game_started = True
        self.current_dice = [] 

    def roll_dice_once(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        return (d1, d2)

    def roll_and_assign_dice(self):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        self.current_dice = [d1, d2]
        self.dice_result = f"({self.current_player}'s turn) Dice: {d1}, {d2}"
        self.selected_piece = None
        self.possible_moves.clear()

    def attempt_select_or_move(self, pos):
        clicked_point, clicked_piece_index = self.find_piece_at(pos)
        if clicked_point:
            piece_color, _, _ = self.board[clicked_point][clicked_piece_index]
            if self.current_player not in piece_color:
                return

            if self.selected_piece:
                spoint, sindex = self.selected_piece
                scolor, shov, ssel = self.board[spoint][sindex]
                self.board[spoint][sindex] = (scolor, shov, False)

            self.selected_piece = (clicked_point, clicked_piece_index)
            pcolor, phov, psel = self.board[clicked_point][clicked_piece_index]
            self.board[clicked_point][clicked_piece_index] = (pcolor, phov, True)

            self.calculate_possible_moves()
        else:
            if self.selected_piece and self.possible_moves:
                spoint, sindex = self.selected_piece
                valid_dest = self.find_move_if_valid(pos, spoint, sindex)
                if valid_dest is not None:
                    self.execute_move(spoint, sindex, valid_dest)

    def find_move_if_valid(self, pos, spoint, sindex):
        for (start_point, piece_index, dest_point) in self.possible_moves:
            if (start_point == spoint) and (piece_index == sindex):
                px, py = self.point_coords[dest_point]
                stack_size = len(self.board[dest_point])
                radius = 15
                stack_offset = 20
                if dest_point <= 12:
                    py = py + stack_size * stack_offset + radius
                else:
                    py = py - stack_size * stack_offset - radius
                dx = pos[0] - px
                dy = pos[1] - py
                if dx*dx + dy*dy <= radius*radius:
                    return dest_point
        return None

    def calculate_possible_moves(self):
        self.possible_moves.clear()
        if not self.selected_piece or not self.current_dice:
            return
        spoint, sindex = self.selected_piece
        color, hov, sel = self.board[spoint][sindex]

        moves = []
        for die in self.current_dice:
            if "white" in color:
                dest = spoint - die
            else:
                dest = spoint + die
            if 1 <= dest <= 24:
                if self.can_land_on(dest, color):
                    moves.append(dest)

        for dest_point in moves:
            self.possible_moves.append((spoint, sindex, dest_point))

    def can_land_on(self, dest_point, piece_color):
        stack = self.board[dest_point]
        if not stack:
            return True
        else:
            other_color_count = 0
            first_stack_color = stack[0][0]
            if piece_color in first_stack_color:
                return True
            else:
                if len(stack) == 1:
                    return True
        return False

    def execute_move(self, spoint, sindex, dest_point):
        piece_color, hov, sel = self.board[spoint][sindex]
        self.board[spoint].pop(sindex)
        if len(self.board[dest_point]) == 1:
            existing_color, ehov, esel = self.board[dest_point][0]
            if existing_color != piece_color:
                self.board[dest_point].clear()
        self.board[dest_point].append((piece_color, False, False))
        self.selected_piece = None
        self.possible_moves.clear()

        used_die = abs(spoint - dest_point)
        if used_die in self.current_dice:
            self.current_dice.remove(used_die)

        if not self.current_dice:
            self.end_turn()

    def end_turn(self):
        if self.current_player == "white":
            self.current_player = "black"
        else:
            self.current_player = "white"
        self.dice_result = f"{self.current_player} turn - throw dice!"

    def find_piece_at(self, pos):
        if not self.game_started:
            return (None, None)
        radius = 15
        stack_offset = 20
        x, y = pos
        for point_idx, stack in self.board.items():
            # For top row
            if point_idx <= 12:
                for i, piece in enumerate(stack):
                    color, hovered, selected = piece
                    px, py = self.point_coords[point_idx]
                    py = py + i * stack_offset + radius
                    dx = x - px
                    dy = y - py
                    dist = dx*dx + dy*dy
                    if dist <= radius*radius:
                        return (point_idx, i)
            else:
                # Bottom row
                for i, piece in enumerate(stack):
                    color, hovered, selected = piece
                    px, py = self.point_coords[point_idx]
                    py = py - i * stack_offset - radius
                    dx = x - px
                    dy = y - py
                    dist = dx*dx + dy*dy
                    if dist <= radius*radius:
                        return (point_idx, i)
        return (None, None)

    def update_hover_states(self):
        if not self.game_started:
            return
        mouse_pos = pygame.mouse.get_pos()
        radius = 15
        stack_offset = 20
        for point_idx, stack in self.board.items():
            new_stack = []
            for i, piece in enumerate(stack):
                color, hovered, selected = piece
                px, py = self.point_coords[point_idx]
                if point_idx <= 12:
                    py = py + i * stack_offset + radius
                else:
                    py = py - i * stack_offset - radius
                dx = mouse_pos[0] - px
                dy = mouse_pos[1] - py
                dist = dx*dx + dy*dy
                is_hover = (dist <= radius*radius) and (self.current_player in color)
                new_stack.append((color, is_hover, selected))
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

def color_map(col):
    if col == "white":
        return (255, 255, 255)
    elif col == "black":
        return (0, 0, 0)
    return (128, 128, 128)

if __name__ == "__main__":
    game_gui = GUI(1200, 800, "Backgammon")
    game_gui.gui_loop()