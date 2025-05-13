from HexBoard import HexBoard
from Player import Player, Agent
import time

class Main():
    def __init__(self):
        self.hexboard = HexBoard()
        self.hexboard.load_puzzle("11")
        
        # Pass color and agent_type when creating Agent instances
        self.player1 = Agent(color="white", agent_type="min_max")
        self.player2 = Agent(color="black", agent_type="random")
        
        self.current_player = self.player1
        self.game_over = False
        self.winner = ""
        self.puzzles = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

    def play(self):
        dictionary = {'white': 0, 'black': 0, 'remise': 0}
        total_games = 1
        start_time = time.time()

        for i in range(total_games):
            print(f"\n🎮 Starting Game {i + 1}")
            print("📌 Initial Board:")
            self.hexboard.print_hexboard()

            while not self.game_over:
                print(f"\n🔁 {self.current_player.color.upper()} ({self.current_player.agent_type}) is making a move...")

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
                    print(f"⏱️  MinMax Move Time: {move_duration:.2f} seconds")

                print(f"✅ Move: {move}")

                opponent = self.player1 if self.current_player == self.player2 else self.player2
                self.game_over, self.winner = self.hexboard.is_game_over(opponent.color)

                self.hexboard.print_hexboard()

                if self.game_over:
                    print(f"\n🏁 Game Over! Winner: {self.winner.upper()}")
                    dictionary[self.winner] += 1
                else:
                    self.current_player = opponent

            self.__init__()  # Reset for next game

        end_time = time.time()
        elapsed_time = end_time - start_time

        print("\n📊 Final Stats:")
        print(f"Total Games Played: {total_games}")
        print(f"White Wins: {dictionary['white']}")
        print(f"Black Wins: {dictionary['black']}")
        print(f"Remise (Draws): {dictionary['remise']}")
        print(f"⏳ Total Time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main = Main()
    main.play()
