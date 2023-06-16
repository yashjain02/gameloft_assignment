import re
import dataclass,enum, staticmethod, classmethod
import datetime
import Enum, Union, List
@enum
class CountryCode:
    FR = 'France'
    US = 'USA'

@dataclass
class Game:
    game_name: str  # unique identifier
    release_date: str

    @classmethod
    def read_games_from_file() -> list:
        games = []
        with open('games.txt', 'r') as file:
            for line in file:
                match = re.search(r'Our game "(.+)" has been released on (.+) on "(\d{4}-\d{2}-\d{2})"', line)
                if match:
                    game_name = match.group(1)
                    release_date = match.group(2)
                    game = Game(game_name, release_date)
                    games.append(game)
        return games

    def has_game_been_released(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        if current_date >= self.release_date:
            return True
        else:
            return False

@dataclass
class Player:
    name: str  # unique identifier
    age: int
    country: Enum
    Games: Union[str, List[str]]

    @classmethod
    def read_players_from_file(cls) -> list:
        players = []
        with open('players.txt', 'r') as file:
            for line in file:
                match = re.search(r'New Player "(.+)" has been registered: Age "(.+)", Country "(.+)", playing "(.+)"', line)
                if match:
                    name = match.group(1)
                    age = int(match.group(2))
                    country = match.group(3)
                    games = match.group(4).split(" and ")
                    player = Player(name=name, age=age, country=CountryCode[country], games=games)
                    players.append(player)
        return players


@dataclass
class Transaction:
    player: Player
    Game: Game
    transaction_date: str
    amount: float

    def is_transaction_valid(self):
        release_date = datetime.strptime(self.game.release_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        transaction_date = datetime.strptime(self.transaction_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        return transaction_date >= release_date

    def is_transaction_recent(self) -> bool:
        transaction_date = datetime.strptime(self.transaction_date, "%Y-%m-%d").date()
        current_date = datetime.now().date()
        return (current_date - transaction_date).days <= 7

    @classmethod
    def read_transactions_from_file() -> list:
        transactions = []
        with open('transactions.txt', 'r') as file:
            for line in file:
                match = re.search(r'Player "(.+)" has made a new transaction for game "(.+)" on the "(\d{4}-\d{2}-\d{2})" for "(.+)"', line)
                if match:
                    player_name = match.group(1)
                    game_name = match.group(2)
                    transaction_date = match.group(3)
                    amount = float(match.group(4))
                    game = Game(game_name=game_name, release_date="", release_source="")
                    player = Player(name=player_name, age=0, country=CountryCode.FR, games=[])
                    transaction = Transaction(player=player, game=game, transaction_date=transaction_date, amount=amount)
                    transactions.append(transaction)
        return transactions

    @staticmethod
    def calculate_revenue(transactions, player) -> float:
        total_revenue = 0.0
        for transaction in transactions:
            if transaction.player == player:
                total_revenue += transaction.amount
        return total_revenue


@dataclass
class RefundableTransaction(Transaction):
    """Add a data member to distinguish between refundable and non-refundable transactions
    """

    @classmethod
    def read_transactions_from_file() -> list:
        transactions = []
        with open('transactions.txt', 'r') as file:
            for line in file:
                match = re.search(r'Player "(.+)" has made a new \(refundable\) transaction for game "(.+)" on the "(\d{4}-\d{2}-\d{2})" for "(.+)"', line)
                if match:
                    player_name = match.group(1)
                    game_name = match.group(2)
                    transaction_date = match.group(3)
                    amount = float(match.group(4))
                    game = Game(game_name=game_name, release_date="", release_source="")
                    player = Player(name=player_name, age=0, country=CountryCode.FR, games=[])
                    transaction = RefundableTransaction(player=player, game=game, transaction_date=transaction_date, amount=amount, refundable=True)
                    transactions.append(transaction)
        return transactions

    def can_refund(self):
        if self.is_transaction_recent() and self.amount > 20 and self.refundable:
            return True
        else:
            return False


def sort_transactions(transactions, sort_by='amount'):
    if sort_by == 'amount':
        transactions.sort(key=lambda t: t.amount)
    elif sort_by == 'transaction_date':
        transactions.sort(key=lambda t: datetime.strptime(t.transaction_date, "%Y-%m-%d"))
    else:
        raise ValueError("Invalid sort_by value. Expected 'amount' or 'transaction_date'.")