class Player:
    def __init__(self, name):
        """
        User's name, though in this game based on lab instructions its default set as "One"
        :param name: Name of the player(user)
        """
        self.name = name
        self.score = 0 #initially set score to 0

    def get_score(self):
        """
        Display current score

        :return: current score
        """
        return self.score

    def add_score(self, score):
        """
        When player scores add it to total score

        :param score: that need to be added
        """
        self.score += score

    def __str__(self):
        """
        String representation of player name and score

        :return: Player score and name
        """
        return f'Player name: {self.name}, Total Score: {self.score}'
