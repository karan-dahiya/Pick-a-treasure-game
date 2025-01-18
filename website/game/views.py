
import random
from django.shortcuts import render, redirect
from .models import Tile, Player
from django.http import HttpResponse
from django.db import transaction


class BoardGenerator:
    def __init__(self, n, t):
        if n <= 0 or t <= 0:
            raise ValueError("Only positive integers")

        self.layoutSize = n
        self.treasureNumber = t
        self.board = [['-' for _ in range(n)] for _ in range(n)]  # A (n*n) board
        self.place_treasures()

    def place_treasures(self):
        """Places treasures randomly on the board"""
        for label in range(1, self.treasureNumber + 1):
            count = label  # Space the treasure value occupies (e.g., 3 for treasure "3")
            placed = False

            while not placed:
                row = random.randint(0, self.layoutSize - 1)
                col = random.randint(0, self.layoutSize - 1)

                if random.choice([True, False]):  # Horizontal placement
                    if col + count <= self.layoutSize:
                        if all(self.board[row][col + i] == '-' for i in range(count)):
                            for i in range(count):
                                self.board[row][col + i] = str(label)
                            placed = True
                else:  # Vertical placement
                    if row + count <= self.layoutSize:
                        if all(self.board[row + i][col] == '-' for i in range(count)):
                            for i in range(count):
                                self.board[row + i][col] = str(label)
                            placed = True

    def pick(self, row, col):
        """Validate and pick the treasure from the board"""
        if row < 0 or row >= self.layoutSize or col < 0 or col >= self.layoutSize:
            raise IndexError("Invalid Points, Does not exist")

        treasure = self.board[row][col]
        if treasure != '-':
            self.board[row][col] = ' '  # Empty the spot after picking
            return int(treasure)
        else:
            return None

    def __str__(self):
        """String representation of the board"""
        return '\n'.join(' '.join(str(item) for item in row) for row in self.board)


def create_game(request):
    """View to create a new game with a 10x10 board and 2 players"""
    board_generator = BoardGenerator(10, 4)

    # Create two players, named "One" and "Two"
    player_one = Player.objects.create(name="One", score=0)
    player_two = Player.objects.create(name="Two", score=0)

    # Create the tiles in the database
    for row in range(10):
        for col in range(10):
            value = board_generator.board[row][col]
            Tile.objects.create(row=row, column=col, value=value)

    # Store board and player data in session
    request.session['board'] = board_generator.board
    request.session['players'] = {
        "One": player_one.id,
        "Two": player_two.id
    }

    # Prepare context for rendering the template
    context = {
        'board': board_generator.__str__(),
        'player_one': player_one,
        'player_two': player_two
    }

    return render(request, 'game/create_game.html', context)

def game_board(request):
    # Retrieve the board and players
    board_data = request.session.get('board')
    if not board_data:
        return HttpResponse("Error: No game created yet. Please create a game first.")

    # Initialize the board with the session data
    board_generator = BoardGenerator(10, 4)
    board_generator.board = board_data

    # Retrieve player scores
    player_one = Player.objects.get(name="One")
    player_two = Player.objects.get(name="Two")

    context = {
        'board': board_generator.__str__(),
        'player_one': player_one,
        'player_two': player_two
    }

    return render(request, 'game/create_game.html', context)

# View to display individual player score (no board)
def player_score(request, player_name):
    try:
        # Get the player by name
        player = Player.objects.get(name=player_name)

        context = {
            'player': player
        }

        return render(request, 'game/player_score.html', context)

    except Player.DoesNotExist:
        return HttpResponse(f"Error: Player {player_name} does not exist.")

@transaction.atomic
def pick_treasure(request, player_name, row, col):
    """Handles a player's pick action and updates the score"""
    try:
        # Retrieve the current board from session
        board_data = request.session.get('board')
        if not board_data:
            return HttpResponse("Error: No game created yet. Please create a game first.")

        # Initialize the board with the session data
        board_generator = BoardGenerator(10, 4)
        board_generator.board = board_data

        # Retrieve players from session
        players_data = request.session.get('players')
        players = Player.objects.filter(name=player_name)

        if players.count() != 1:
            return HttpResponse(f"Error: Player with name {player_name} not found or multiple players with the same name exist. Please ensure player names are unique.")

        player = players.first()  # Get the first player from the filtered queryset

        # Validate the row and column inputs
        if not (0 <= row < board_generator.layoutSize and 0 <= col < board_generator.layoutSize):
            return HttpResponse(f"Error: Invalid row ({row}) or column ({col}). The valid range is from 0 to {board_generator.layoutSize - 1}.")

        # Process the pick
        treasure = board_generator.board[row][col]

        # Check if the tile has a treasure or is empty
        if treasure != '-' and treasure != ' ':
            # Tile has a treasure
            score = int(treasure)  # Convert the treasure value to integer
            player.score += score  # Update the player score
            player.save()

            # Empty the tile after picking the treasure
            board_generator.board[row][col] = ' '  # Set the position to empty after pick

            # Save updated board to session
            request.session['board'] = board_generator.board

            message = f'{player_name} picked a treasure and earned {score} points!'
        else:
            # Tile is empty or invalid (already picked previously)
            message = f'{player_name} picked an empty spot. No points earned.'

        # Prepare context for rendering the updated board and scores
        context = {
            'board': board_generator.__str__(),
            'player_one': Player.objects.get(name="One"),
            'player_two': Player.objects.get(name="Two"),
            'message': message
        }

        return render(request, 'game/create_game.html', context)

    except Player.DoesNotExist:
        return HttpResponse(f"Error: Player {player_name} does not exist.")
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}")