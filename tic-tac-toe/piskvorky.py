import pygame
import sys
import random
import time

class PiskvorkyGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
                
        # Detection of screen width and height
        display_info = pygame.display.Info() 
        screen_width, screen_height = display_info.current_w, display_info.current_h
        
        # Monitor settings - manually because of exact square size, took the most common monitor resolutions, other option is to set the window width and height as partitions of screen width and height
        if screen_width == 3840 and screen_height == 2160: # 4K
            self.width, self.height = 980, 1100
            
            # Definition of dimensions of the game field
            self.line_width =           5
            self.win_line_width =       5
            self.board_rows =           14
            self.board_cols =           14
            self.square_size =          int(((self.width + self.height)) // (self.board_cols + self.board_rows))
            self.circle_radius =        self.square_size // 3
            self.circle_width =         15
            self.cross_width =          25
            self.space =                self.square_size // 4
            self.info_box_height =      101
            self.info_text_y =          50
            self.playing_text_y =       50
        
        if screen_width == 2560 and screen_height == 1440: # 2K
            self.width, self.height = 1092, 1187
            
            # Definition of dimensions of the game field
            self.line_width =           5
            self.win_line_width =       5
            self.board_rows =           14
            self.board_cols =           14
            self.square_size =          int(((self.width + self.height) * 0.97) // (self.board_cols + self.board_rows))
            self.circle_radius =        self.square_size // 3
            self.circle_width =         15
            self.cross_width =          25
            self.space =                self.square_size // 4
            self.info_box_height =      92
            self.info_text_y =          50
            self.playing_text_y =       50
            
        if screen_width == 1920 and screen_height == 1080: # FULL HD
            self.width, self.height = 895, 1000
        
            # Definition of dimensions of the game field
            self.line_width =           5
            self.win_line_width =       5
            self.board_rows =           14
            self.board_cols =           14
            self.square_size =          int(((self.width + self.height) * 0.95) // (self.board_cols + self.board_rows))
            self.circle_radius =        self.square_size // 3
            self.circle_width =         15
            self.cross_width =          25
            self.space =                self.square_size // 4
            self.info_box_height =      101
            self.info_text_y =          50
            self.playing_text_y =       50
        
        # Definition of colors 
        self.names_color =              (28, 170, 156)
        self.background_color =         (28, 170, 156)
        self.show_information_color =   (28, 170, 156)
        self.line_color =               (23, 145, 135)
        self.circle_color =             (239, 231, 200)
        self.cross_color =              (84, 84, 84)
        self.WHITE =                    (255, 255, 255)
        self.BLACK =                    (0, 0, 0)
        self.GREEN =                    (0, 255, 0)
        
        # Definition of fonts
        self.font = pygame.font.Font(None, 55)
        self.playing_font = pygame.font.Font(None, 60)
        self.name_font = pygame.font.Font(None, 50)
        self.information_font = pygame.font.SysFont("Arial", 20)
        self.information_bold_font = pygame.font.SysFont("Arial", 20, bold = True)
        
        # Creation of the main window
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("TIC-TAC-TOE")
        self.screen.fill(self.background_color)
        self.board = [[0] * self.board_cols for _ in range(self.board_rows)]
        
        # Starting the menu function
        self.menu()
    
    # Function for random picking who is playing first
    def player_picker(self, game, player_name = None, player1_name = None, player2_name = None):
        self.game_choice = game
        if self.game_choice == "single":
            # Settings of players (game for one)
            self.game_over = False
            self.player_name = player_name
            self.bot_name = "Bot"
            players = [self.player_name, self.bot_name]
            self.current_player_name = random.choice(players)
            if self.current_player_name == self.player_name:
                self.current_player = 1
            else:
                self.current_player = 2
           
        elif self.game_choice == "double":
            # Settings of players (game for two)
            self.game_over = False
            self.player1_name = player1_name
            self.player2_name = player2_name
            players = [self.player1_name, self.player2_name]
            self.current_player_name = random.choice(players)
            if self.current_player_name == self.player1_name:
                self.current_player = 1
            else:
                self.current_player = 2
        
    # Function for displaying the text in the info box
    def display_text(self, text, position, color, font):
        text_surface = font.render(text, True, color)
        self.text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, self.text_rect)
    
    # Function for clearing the text from info box
    def info_box(self):
        clear_rect = pygame.Rect(0, self.height - self.info_box_height, self.width, self.info_box_height,) 
        pygame.draw.rect(self.screen, self.background_color, clear_rect)
    
    # Menu screen
    def menu(self):
        self.screen.fill(self.background_color)
        self.display_text("TIC-TAC-TOE", (self.width // 2, self.height // 3 - 100), color = self.BLACK, font = self.name_font)
        self.display_text("Start New Game", (self.width // 2, self.height // 3), color = self.WHITE, font = self.name_font)
        self.display_text("Information", (self.width // 2, self.height // 3 + 50), color = self.WHITE, font = self.name_font)
        self.display_text("Exit", (self.width // 2, self.height // 3 + 100), color = self.WHITE, font = self.name_font)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if self.width // 2 - 150 < mouseX < self.width // 2 + 150:
                        if self.height // 3 - 25 < mouseY < self.height // 3 + 25:
                            self.game_type()
                            return
                        elif self.height // 3 + 25 < mouseY < self.height // 3 + 75:
                            self.show_information()
                            return
                        elif self.height // 3 + 75 < mouseY < self.height // 3 + 125:
                            pygame.quit()
                            sys.exit()
    
    # Function for picking the type of game (single, double)
    def game_type(self):
        self.screen.fill(self.background_color)
        self.display_text("Game for One Player", (self.width // 2, self.height // 3), color = self.WHITE, font = self.name_font)
        self.display_text("Game for Two Players", (self.width // 2, self.height // 3 + 50), color = self.WHITE, font = self.name_font)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if self.width // 2 - 150 < mouseX < self.width // 2 + 150:
                        if self.height // 3 - 25 < mouseY < self.height // 3 + 25:
                            self.name_n_play()
                            return
                        elif self.height // 3 + 25 < mouseY < self.height // 3 + 75:
                            self.names_n_play()
                            return
                        elif self.height // 3 + 75 < mouseY < self.height // 3 + 125:
                            pygame.quit()
                            sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.menu()
                            
    # Asking for the name of player 
    def name_n_play(self):
        self.screen.fill(self.names_color)
        self.player_name = self.get_text_input(1, game_choice = "single")
        self.player_picker(game = "single", player_name = self.player_name)
        self.screen.fill(self.background_color)
        self.clear_board()
        self.draw_lines()
        self.draw_symbols()
        self.info_box()
        text_surface = self.font.render(f"{self.current_player_name} is first to make a move!", True, self.GREEN)
        text_rect = text_surface.get_rect(center = (self.width // 2, self.height - 50))
        self.screen.blit(text_surface, text_rect)
        self.run()
    
    # Asking for the names of both players     
    def names_n_play(self):
        self.screen.fill(self.names_color)
        self.player1_name = self.get_text_input(1, game_choice = "double")
        self.player2_name = self.get_text_input(2, game_choice = "double")
        self.player_picker(game = "double", player1_name = self.player1_name, player2_name = self.player2_name)
        self.screen.fill(self.background_color)
        self.clear_board()
        self.draw_lines()
        self.draw_symbols()
        self.info_box()
        self.run()                      
    
    # Getting the text from the player input
    def get_text_input(self, player_num, game_choice):
        input_box = pygame.Rect(self.width // 2.55, self.height // 2.7, self.width // 2, 50)
        color_inactive = pygame.Color("grey")
        color_active = pygame.Color("black")
        color = color_inactive
        active = False
        text = ""
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m and active == False:
                        self.menu()
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            if game_choice == "double":                
                self.screen.fill(self.names_color)
                self.display_text(f"Enter name for Player {player_num}: ", (self.width // 2, self.height // 3), color = self.BLACK, font = self.font)
            else:
                self.screen.fill(self.names_color)
                self.display_text(f"Enter name for Player: ", (self.width // 2, self.height // 3), color = self.BLACK, font = self.font)

            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            pygame.display.flip()
            clock.tick(60)
                                
    def render_multi_line_text(self, screen, text, position, font, max_width, color):
        lines = []
        words = text.split(' ')
        current_line = ''

        for word in words:
            test_line = f'{current_line} {word}'.strip()
            test_surface = font.render(test_line, True, color)
            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        x, y = position
        for line in lines:
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (x, y))
            y += text_surface.get_height()
    
    # Showing information about the game
    def show_information(self):
        text0 = ("This is a game of Piskvorky (Tic-Tac-Toe).")
        text1 = ("The objective is to align five of your symbols in a row, either "
               "horizontally, vertically, or diagonally. "
               "The game is played on a 14x14 grid, with Player 1 using circles (O) "
               "and Player 2 uses crosses (X). "
               "Players take turns placing their symbols: Player 1 uses the Left "
               "Mouse Button (LMB), while Player 2 uses the Right Mouse Button (RMB). "
               "To win, you need to align five of your symbols next to each other. The game "
               "ends when a player forms such a line or the grid is completely filled, "
               "resulting in a draw. "
               "You can restart the game at any time by pressing the 'R' key. Enter "
               "your names at the beginning, which will be displayed during your turns. "
               "Use the interactive menu to start a new game, view game information, "
               "or exit. Be strategic: block your opponent while creating your own row "
               "of five. Enjoy and may the best player win!")
        text2 = ("Important key shortcuts: ")
        text3 = ("Press 'M' to go back to the Main Menu.")
        text4 = ("Press 'R' inside the game to restart the game.")
        
        position0 = (200, 150)
        position1 = (200, 175)
        position2 = (200, 500)
        position3 = (200, 525)
        position4 = (200, 550)
        
        self.screen.fill(self.show_information_color)
        self.render_multi_line_text(self.screen, text0, position0, font = self.information_bold_font, max_width = self.width - 400, color = self.BLACK)
        self.render_multi_line_text(self.screen, text1, position1, font = self.information_font, max_width = self.width - 400, color = self.BLACK)
        self.render_multi_line_text(self.screen, text2, position2, font = self.information_bold_font, max_width = self.width - 400, color = self.BLACK)
        self.render_multi_line_text(self.screen, text3, position3, font = self.information_font, max_width = self.width - 400, color = self.BLACK)
        self.render_multi_line_text(self.screen, text4, position4, font = self.information_font, max_width = self.width - 400, color = self.BLACK)      
        
        self.display_text("Important Information about the Game", (self.width // 2, self.height * 0.1), color = self.BLACK, font = self.name_font)
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = event.pos
                    if self.width // 2 - 150 < mouseX < self.width // 2 + 150:
                        if self.height // 3 - 125 < mouseY < self.height // 3 - 75:
                            self.menu()
                            return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.menu()        

    # Drawing all the lines
    def draw_lines(self):
        for i in range(self.board_rows):
            pygame.draw.line(self.screen, self.line_color, (0, (i + 1) * self.square_size), (self.width, (i + 1) * self.square_size), self.line_width)

        for j in range(self.board_cols - 1):
            pygame.draw.line(self.screen, self.line_color, ((j + 1) * self.square_size, 0), ((j + 1) * self.square_size, self.height), self.line_width)

    # Drawing either circles or crosses
    def draw_symbols(self):
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, self.circle_color, (int(col * self.square_size + self.square_size // 2), int(row * self.square_size + self.square_size // 2)), self.circle_radius, self.circle_width)
                elif self.board[row][col] == 2:
                    pygame.draw.line(self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.square_size - self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.space), self.cross_width)
                    pygame.draw.line(self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.square_size - self.space), self.cross_width)

    # Checking possible win
    def check_win(self, player):
        for col in range(self.board_cols):
            for row in range(self.board_rows):
                if row + 4 < self.board_rows:
                    if self.board[row][col] == player and self.board[row + 1][col] == player and self.board[row + 2][col] == player and self.board[row + 3][col] == player and self.board[row + 4][col] == player:
                        self.draw_vertical_winning_line(row, col, player)
                        return True

        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if col + 4 < self.board_cols:
                    if self.board[row][col] == player and self.board[row][col + 1] == player and self.board[row][col + 2] == player and self.board[row][col + 3] == player and self.board[row][col + 4] == player:
                        self.draw_horizontal_winning_line(row, col, player)
                        return True

        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if (self.board_rows - 1) - row - 3 > 0 and col + 4 < self.board_cols:
                    if self.board[(self.board_rows - 1) - row][col] == player and self.board[(self.board_rows - 1) - row - 1][col + 1] == player and self.board[(self.board_rows - 1) - row - 2][col + 2] == player and self.board[(self.board_rows - 1) - row - 3][col + 3] == player and self.board[(self.board_rows - 1) - row - 4][col + 4] == player:
                        self.draw_asc_diagonal(row, col, player)
                        return True

        for row in range(self.board_rows):
            for col in range(self.board_cols):
                if row + 4 < self.board_rows and col + 4 < self.board_cols:
                    if self.board[row][col] == player and self.board[row + 1][col + 1] == player and self.board[row + 2][col + 2] == player and self.board[row + 3][col + 3] == player and self.board[row + 4][col + 4] == player:
                        self.draw_desc_diagonal(row, col, player)
                        return True

        return False

    # Drawing all the winning lines
    def draw_vertical_winning_line(self, row, col, player):
        posX = col * self.square_size + self.square_size // 2
        posY = row * self.square_size + self.square_size // 2
        color = self.circle_color if player == 1 else self.cross_color
        pygame.draw.line(self.screen, color, (posX, posY), (posX, self.square_size*4 + posY), self.win_line_width)

    def draw_horizontal_winning_line(self, row, col, player):
        posX = col * self.square_size + self.square_size // 2
        posY = row * self.square_size + self.square_size // 2
        color = self.circle_color if player == 1 else self.cross_color
        pygame.draw.line(self.screen, color, (posX, posY), (self.square_size*4 + posX, posY), self.win_line_width)

    def draw_asc_diagonal(self, row, col, player):
        posX1 = col * self.square_size + self.square_size // 2
        posY1 = ((self.board_rows - 1) - row) * self.square_size + self.square_size // 2
        posX2 = (col + 4) * self.square_size + self.square_size // 2
        posY2 = ((self.board_rows - 1) - row - 4) * self.square_size + self.square_size // 2
        color = self.circle_color if player == 1 else self.cross_color
        pygame.draw.line(self.screen, color, (posX1, posY1), (posX2, posY2), self.win_line_width)

    def draw_desc_diagonal(self, row, col, player):
        posX1 = col * self.square_size + self.square_size // 2
        posY1 = row * self.square_size + self.square_size // 2
        posX2 = (col + 4) * self.square_size + self.square_size // 2
        posY2 = (row + 4) * self.square_size + self.square_size // 2
        color = self.circle_color if player == 1 else self.cross_color
        pygame.draw.line(self.screen, color, (posX1, posY1), (posX2, posY2), self.win_line_width)

    # Display the winner
    def display_winner(self, winner, game):
        if game == "single":
            if winner == 1:
                text = f"{self.player_name} Wins!"
            elif winner == 2:
                text = f"{self.bot_name} Wins!"
            elif winner == "draw":
                text = "It is a Draw"
        elif game == "double":
            if winner == 1:
                text = f"{self.player1_name} Wins!"
            elif winner == 2:
                text = f"{self.player2_name} Wins!"
            elif winner == "draw":
                text = "It is a Draw"
        
        self.info_box()
        text_surface = self.font.render(text, True, self.GREEN)
        text_rect = text_surface.get_rect(center = (self.width // 2, self.height - 50))

        self.screen.blit(text_surface, text_rect)
        
    # Definition of function for clearing the board
    def clear_board(self):
        self.board = [[0] * self.board_cols for _ in range(self.board_rows)]

    # Definition of function for restarting the game 
    def restart(self):
        self.screen.fill(self.background_color)
        self.clear_board()
        if self.game_choice == "single":
            self.player_picker(game = self.game_choice, player_name = self.player_name)
            self.draw_lines()
            self.info_box()
            text_surface = self.font.render(f"{self.current_player_name} is first to make a move!", True, self.GREEN)
            text_rect = text_surface.get_rect(center = (self.width // 2, self.height - 50))
            self.screen.blit(text_surface, text_rect)
            self.draw_symbols()  
        else:
            self.player_picker(game = self.game_choice, player1_name = self.player1_name, player2_name = self.player2_name)  
            self.draw_lines()
            self.info_box()
            self.draw_symbols()
        
    # Definition of function for full board detection
    def is_board_full(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    # Definition of function for evaluating move based on winning and blocking potential
    def evaluate_move(self, board, move, player):
        opponent = 1 # The player himself represented by number 1 and acting as an opponent for the PC BOT
        score = 0
        
        board[move] = player
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for d in directions:
            player_count = self.count_in_direction(board, move, player, d)
            opponent_count = self.count_in_direction(board, move, opponent, d)
            
            # Potential moves awarded with prizes
            # Potential series of PC bot
            if player_count == 5:
                score += 200
            elif opponent_count == 4:
                score += 150
            elif player_count == 4:
                score += 120
            elif opponent_count == 3:
                score += 90 
            elif player_count == 3:
                score += 60
            elif player_count == 2:
                score += 30
            elif opponent_count == 2:
                score += 10         
        
        # Reset the move
        board[move] = ''
        
        return score
    
    # Definition of function for counting consecutive pieces in a given direction
    def count_in_direction(self, board, start, player, direction):
        count = 1
        row, col = divmod(start, self.board_rows)
            
        # Check in both directions
        for dir_mul in [-1, 1]:
            for i in range(1, 5):
                r = row + direction[0] * i * dir_mul
                c = col + direction[1] * i * dir_mul
                if 0 <= r < self.board_rows and 0 <= c < self.board_rows and board[r * self.board_rows + c] == player:
                    count += 1
                else:
                    break
        
        return count
    
    # Find the best move by evaluating all possible moves
    def best_move(self, board, player):
        best_score = -float('inf')
        best_move = None
        board = [item for sublist in board for item in sublist]

        if sum(board) == 0:
            best_move = int((self.board_rows**2)/2 + 7)
        else:
            for i in range(self.board_rows * self.board_cols):
                if board[i] == 0:                     
                    move_score = self.evaluate_move(board, i, player)
                    if move_score > best_score:
                        best_score = move_score
                        best_move = i
                        
        return best_move
        
    # Definition of function for running the game itself
    def run(self):
        if self.game_choice == "double":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if not self.game_over and self.game_choice == "double":
                        if not self.check_win(1) and not self.check_win(2):
                            self.info_box()
                        if self.current_player == 1 and not self.check_win(1):
                            self.display_text(f"{self.player1_name} is playing! (LMB)", (self.width // 2, self.height - self.playing_text_y), color = self.WHITE, font = self.playing_font)
                        elif self.current_player == 2 and not self.check_win(2):
                            self.display_text(f"{self.player2_name} is playing! (RMB)", (self.width // 2, self.height - self.playing_text_y), color = self.WHITE, font = self.playing_font)   
                        
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]

                        clicked_row = mouseY // self.square_size
                        clicked_col = mouseX // self.square_size

                        if self.current_player == 1 and event.button == 1:
                            if 0 <= clicked_row < self.board_rows and 0 <= clicked_col < self.board_cols:
                                if self.board[clicked_row][clicked_col] == 0:
                                    self.board[clicked_row][clicked_col] = 1
                                    self.draw_symbols()
                                    if self.check_win(1):
                                        self.game_over = True
                                        self.display_winner(1, game = self.game_choice)
                                    else:
                                        if self.is_board_full():
                                            self.display_text("draw")
                                            self.game_over = True
                                    self.current_player = 2

                        elif self.current_player == 2 and event.button == 3: 
                            if 0 <= clicked_row < self.board_rows and 0 <= clicked_col < self.board_cols:
                                if self.board[clicked_row][clicked_col] == 0:
                                    self.board[clicked_row][clicked_col] = 2
                                    self.draw_symbols()
                                    if self.check_win(2):
                                        self.game_over = True
                                        self.display_winner(2, game = self.game_choice)
                                    else:
                                        if self.is_board_full():
                                            self.display_text("draw")
                                            self.game_over = True
                                    self.current_player = 1  
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart()
                            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.menu()

                pygame.display.update()
                
        elif self.game_choice == "single":
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()  
                        
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]

                        clicked_row = mouseY // self.square_size
                        clicked_col = mouseX // self.square_size

                        if self.current_player == 1 and event.button == 1:
                            self.info_box()
                            if 0 <= clicked_row < self.board_rows and 0 <= clicked_col < self.board_cols:
                                if self.board[clicked_row][clicked_col] == 0:
                                    self.board[clicked_row][clicked_col] = 1
                                    self.draw_symbols()
                                    if self.check_win(1):
                                        self.display_winner(1, game = self.game_choice)
                                        self.game_over = True
                                    else:
                                        if self.is_board_full():
                                            self.display_winner("draw")
                                            self.game_over = True
                                    self.current_player = 2

                    if self.current_player == 2 and not self.game_over:  
                        
                        move = self.best_move(board = self.board, player = self.current_player)
                        clicked_row, clicked_col = divmod(move, self.board_rows)
                        self.info_box()                        
                        if self.board[clicked_row][clicked_col] == 0:
                            self.board[clicked_row][clicked_col] = 2
                            self.draw_symbols()
                            if self.check_win(2):
                                self.display_winner(2, game = self.game_choice)
                                self.game_over = True
                            else:
                                if self.is_board_full():
                                    self.display_winner("draw")
                                    self.game_over = True
                            self.current_player = 1  
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.restart()
                            
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.menu()

                pygame.display.update()

if __name__ == "__main__":
    game = PiskvorkyGame()
    game.run()
