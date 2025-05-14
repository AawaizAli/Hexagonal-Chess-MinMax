import pygame
import pygame_gui
from pygame_gui.elements import UITextBox
import time
from HexBoard import HexBoard
from Player import Player, Agent

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BOARD_COLOR = (240, 230, 200)
DARK_GRAY = (100, 100, 100)

class Main():
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        
        # Set up the display
        self.screen_width, self.screen_height = 1200, 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("HexBoard Game")
        
        # Set up GUI manager
        self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        
        # Create text box for output (moved to right side)
        self.output_textbox = UITextBox(
            html_text="",
            relative_rect=pygame.Rect(600, 20, 560, 760),
            manager=self.manager
        )
        
        # Initialize game components
        self.hexboard = HexBoard()
        self.hexboard.load_puzzle("11")
        
        # Pass color and agent_type when creating Agent instances
        self.player1 = Agent(color="white", agent_type="min_max")
        self.player2 = Agent(color="black", agent_type="random")
        
        self.current_player = self.player1
        self.game_over = False
        self.winner = ""
        self.puzzles = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        
        # Game state variables
        self.running = True
        self.clock = pygame.time.Clock()
        self.game_started = False
        self.current_game = 0
        
        # Board drawing parameters (dynamic calculation for centering)
        self.rows = 21
        self.cols = 11
        # Calculate max hex size to fit board in left half
        left_width = self.screen_width // 2
        left_height = self.screen_height
        max_hex_width = left_width / (self.cols * 1.5 + 0.5)
        max_hex_height = left_height / (self.rows * 1.3 + 0.5)
        self.hex_size = int(min(max_hex_width, max_hex_height))
        self.board_width = self.cols * self.hex_size * 1.5
        self.board_height = self.rows * self.hex_size * 1.3
        self.board_offset_x = (left_width - self.board_width) // 2 + 10
        self.board_offset_y = (left_height - self.board_height) // 2
        
        # Initial output
        self.add_output("🎮 HexBoard Game - PyGUI Version")
        self.add_output("Press SPACE to start the game...")

    def draw_hexagon(self, x, y, color, border_color=None):
        """Draw a hexagon at the specified position"""
        points = []
        for i in range(6):
            angle = i * 60
            px = x + self.hex_size * 0.866 * pygame.math.Vector2(1, 0).rotate(angle).x
            py = y + self.hex_size * 0.866 * pygame.math.Vector2(1, 0).rotate(angle).y
            points.append((px, py))
        
        pygame.draw.polygon(self.screen, color, points)
        if border_color:
            pygame.draw.polygon(self.screen, border_color, points, 2)

    def draw_board(self):
        """Draw the hexagonal chess board"""
        # Draw board background with padding
        padding = 20
        left_width = self.screen_width // 2
        left_height = self.screen_height
        pygame.draw.rect(self.screen, BOARD_COLOR, 
                        (0, 0, left_width, left_height))
        
        # Draw hexagons and pieces
        for row in range(self.rows):
            for col in range(self.cols):
                if self.hexboard.hexboard[row][col] is not None:
                    x = self.board_offset_x + col * self.hex_size * 1.5
                    y = self.board_offset_y + row * self.hex_size * 1.3
                    
                    # Draw hexagon with alternating colors
                    hex_color = GRAY if (row + col) % 2 == 0 else (220, 220, 220)
                    self.draw_hexagon(x, y, hex_color, DARK_GRAY)
                    
                    # Draw piece if present
                    piece = self.hexboard.get_piece(row, col)
                    if piece is not None:
                        # Draw piece circle with border
                        piece_color = WHITE if piece.color == "white" else BLACK
                        border_color = BLACK if piece.color == "white" else WHITE
                        pygame.draw.circle(self.screen, piece_color, 
                                        (int(x), int(y)), self.hex_size//2 - 3)
                        pygame.draw.circle(self.screen, border_color, 
                                        (int(x), int(y)), self.hex_size//2 - 3, 2)
                        
                        # Draw piece symbol with improved visibility
                        font = pygame.font.SysFont('Arial', 22, bold=True)
                        piece_text = font.render(piece.name, True, 
                                              BLACK if piece.color == "white" else WHITE)
                        text_rect = piece_text.get_rect(center=(x, y))
                        self.screen.blit(piece_text, text_rect)

    def add_output(self, text):
        """Add text to the output textbox and print to console for verification"""
        print(text)  # Also print to console to verify it matches original
        current_text = self.output_textbox.html_text
        if current_text:
            current_text += "<br>" + text
        else:
            current_text = text
        self.output_textbox.html_text = current_text
        self.output_textbox.rebuild()

    def get_board_text(self):
        """Get the board representation as text"""
        import io
        from contextlib import redirect_stdout
        
        # Capture the print output
        f = io.StringIO()
        with redirect_stdout(f):
            self.hexboard.print_hexboard()
        return f.getvalue()

    def play(self):
        dictionary = {'white': 0, 'black': 0, 'remise': 0}
        total_games = 1
        start_time = time.time()

        while self.running:
            time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_started:
                        self.game_started = True
                        self.add_output("Starting game...")
                
                self.manager.process_events(event)
            
            if self.game_started and not self.game_over:
                if self.current_game < total_games:
                    self.add_output(f"\n🎮 Starting Game {self.current_game + 1}")
                    self.add_output("📌 Initial Board:")
                    self.add_output(self.get_board_text())

                    while not self.game_over:
                        self.add_output(f"\n🔁 {self.current_player.color.upper()} ({self.current_player.agent_type}) is making a move...")

                        if self.current_player.agent_type == "random":
                            move = self.current_player.get_random_move(self.hexboard)
                            self.hexboard.move_piece(move, final=True)
                        elif self.current_player.agent_type == "min_max":
                            move_timer_start = time.time()
                            move = self.current_player.find_min_max_move(
                                self.hexboard,
                                self.current_player.color,
                                use_multiprocessing=True,
                                use_alpha_beta=True
                            )
                            self.hexboard.move_piece(move, final=True)
                            move_timer_end = time.time()
                            move_duration = move_timer_end - move_timer_start
                            self.add_output(f"⏱️  MinMax Move Time: {move_duration:.2f} seconds")

                        self.add_output(f"✅ Move: {move}")

                        opponent = self.player1 if self.current_player == self.player2 else self.player2
                        self.game_over, self.winner = self.hexboard.is_game_over(opponent.color)

                        self.add_output(self.get_board_text())

                        if self.game_over:
                            self.add_output(f"\n🏁 Game Over! Winner: {self.winner.upper()}")
                            dictionary[self.winner] += 1
                            self.current_game += 1
                            
                            if self.current_game < total_games:
                                # Reset for next game
                                self.__init__()
                                self.game_started = True
                            else:
                                # All games finished
                                end_time = time.time()
                                elapsed_time = end_time - start_time
                                
                                self.add_output("\n📊 Final Stats:")
                                self.add_output(f"Total Games Played: {total_games}")
                                self.add_output(f"White Wins: {dictionary['white']}")
                                self.add_output(f"Black Wins: {dictionary['black']}")
                                self.add_output(f"Remise (Draws): {dictionary['remise']}")
                                self.add_output(f"⏳ Total Time: {elapsed_time:.2f} seconds")
                        else:
                            self.current_player = opponent

            self.manager.update(time_delta)
            
            # Draw everything
            self.screen.fill((240, 240, 240))
            self.draw_board()  # Draw the hexagonal board
            self.manager.draw_ui(self.screen)
            
            pygame.display.update()
        
        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.play()
