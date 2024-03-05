import random
from time import sleep
import os


suit_unicode_dict = {'Spades': 'A', 'Hearts': 'B', 'Diamonds': 'C', 'Clubs': 'D'}
rank_unicode_dict = {'Two':'2', 'Three':'3', 'Four':'4', 'Five':'5', 'Six':'6', 
                   'Seven':'7', 'Eight':'8', 'Nine':'9', 'Ten':'A', 'Jack':'B', 'Queen':'C', 'King':'D', 'Ace':'1'}


class Card():
    '''
    Card Class
    '''
    def __init__(self, rank, suit):
        rank_value_dict = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 
                           'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':1}
        self.rank = rank
        self.suit = suit
        self.value = rank_value_dict[rank]
        
    def __str__(self):
        return chr(int(f'0x0001F0{suit_unicode_dict[self.suit]}{rank_unicode_dict[self.rank]}', base=16))
    
    def __repr__(self):
        return chr(int(f'0x0001F0{suit_unicode_dict[self.suit]}{rank_unicode_dict[self.rank]}', base=16))
    
card1 = Card('King', 'Spades')
print(f'{card1}, {card1.value}, {card1.__repr__()}')


class Deck():
    '''
    Deck Class:
        - contains x number of decks (52 cards / deck)
        - shuffle():
            - sorts the cards in the deck
        - draw_card():
            - draws a card from the top of the deck and returns that Card object
    '''
    def __init__(self, number_of_decks):
        ranks = ['Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.number_of_decks = number_of_decks
        self.cards = []
        
        for suit in suits:
            for rank in ranks:
                for i in range(self.number_of_decks):
                    self.cards.append(Card(rank, suit))
                    
    def draw_card(self):
        return self.cards.pop(0)
                    
    def shuffle(self):    
        random.shuffle(self.cards)
        
    def __str__(self):
        return f'{self.number_of_decks} decks with {len(self.cards)} in it'
     

class Hand():
    '''
    Hand class
        - contains a number of cards
    '''    
    def __init__(self):
        self.cards = []
        self.bust = False
        self.natural_blackjack = False
    
    @property
    def value(self):
        value = 0
        for card in self.cards:
            value += card.value
        return value
    
    def add_card(self, deck):
        self.cards.append(deck.draw_card())
        self.optimize_aces()
        if self.value > 21:
            self.bust = True
        elif self.value == 21 and len(self.cards) == 2:
            self.natural_blackjack = True
            
    def optimize_aces(self):
        for card in self.cards:
            if card.rank == 'Ace' and card.value == 1:
                if self.value + 10 <= 21:
                    card.value = 11
                    break
            if card.rank == 'Ace' and card.value == 11 and self.value > 21:
                card.value = 1
                
    def clear_cards(self):
        self.cards.clear()
        self.bust = False
        self.natural_blackjack = False
                
    def __str__(self):
        return f'hand has {self.cards}'
    
    
class Player():
    '''
    Player Class:
        - player has a hand and an amount of money to bet
        - bet():
            - bets a certain amount of money which
    '''
    def __init__(self, money, name):
        self.name = name
        self.money = money
        self.hand = Hand()
        
    def bet(self, amount):
        self.wager = amount


class Blackjack():
        '''
        Blackjack Class:
            - runner class used to run the games
            - deal(deck, players):
                - draws a card from the deck and distributes one card to each player
            - bet(players):
                - asks for a bet from each player
            - player_turn(deck, player):
                - goes through a player turn, asking them to hit or stay
            - house_turn():
                - automatically draws and stays the house based on the number of cards
            - find_winner():
                - calculates winners and winnings for each player
            - print_hands():
                - prints all players' and the house's hands
            - main():
                - main function for running the game
        '''            
        def deal(self, deck, players):
            for player in players:
                player.hand.add_card(deck)
                
        def bet(self, players):
            for player in players:
                player.bet(int(input(f'{player.name} - Enter an amount of money to bet between $2-$500: ')))
            
        def player_turn(self, deck, player):
            while True:
                
                choice = input(f"{player.name} - Your hand is: {player.hand.cards} with value {player.hand.value}. Would you like to hit or stay. Type 1 for hit, and 0 for stay:") == '1'
                
                if choice:
                    player.hand.add_card(deck)
                    if player.hand.bust:
                        print(f'{player.name} has busted with {player.hand.cards} with a value of {player.hand.value}')
                        sleep(3)
                        return False
                    elif player.hand.value == 21:
                        print(f'{player.name} has gotten blackjack with {player.hand.cards}')
                        sleep(3)
                        return True
                else:
                    print(f'{player.name} stays with {player.hand.cards} with a value of {player.hand.value}')
                    sleep(3)
                    return True
        
        def house_turn(self, deck, house):
            '''Continues to choose a new card
            until the computer busts or the comp_sum becomes 17 or higher. It then returns the comp_sum.'''
            while True:
                if house.value < 17:
                    house.add_card(deck)
                    if house.value > 21:
                        print(f'The house has busted with {house.cards} with a value of {house.value}')
                        return False
                else:
                    print(f'The house stays with {house.cards} with a value of {house.value}')
                    return True
        
        def find_winner(self, players, house):
            for player in players:
                if player.hand.bust:
                    player.money -= player.wager
                    print(f'{player.name} busted with {player.hand.cards}: -${player.wager} -> ${player.money}')
                elif player.hand.natural_blackjack:
                    player.money += int(player.wager * 1.5)
                    print(f'{player.name} got a natural blackjack with {player.hand.cards}: +${int(1.5 * player.wager)} -> ${player.money}')
                else:
                    if house.bust:
                        player.money += player.wager
                        print(f'{player.name} wins with {player.hand.cards}: +${player.wager} -> ${player.money}')
                    elif player.hand.value > house.value:
                        player.money += player.wager
                        print(f'{player.name} wins with {player.hand.cards}: +${player.wager} -> ${player.money}')
                    elif player.hand.value == house.value:
                        print(f'{player.name} ties with {player.hand.cards}: +$0 -> ${player.money}')
                    else:
                        player.money -= player.wager
                        print(f'{player.name} loses with {player.hand.cards}: -${player.wager} -> ${player.money}')
                    player.wager = 0
        
        def print_hands(self, players, house):
            for player in players:
                print(f'{player.name}: {player.hand.cards} = {player.hand.value}', end='    ')
            print(f'House: [{house.cards[0]}, ?] = {house.cards[0].value} + ?\n')
        
        def main(self):
            with open('splash_screen.txt') as f:
                splash_art = f.read()
                print(splash_art)
                sleep(2)
                clear_screen()
                
            names = []
            while True:
                print("Join the game! (type 'x' if you are done adding players)\n")
                player_name = input("Input Player Name: ")
                if player_name == 'x':
                    clear_screen()
                    break
                wealth = int(input("Input Player Wealth: "))
                clear_screen()
                names.append((wealth, player_name))
                
            players = [Player(name[0], name[1]) for name in names]
                
            house = Hand()
                
            # create a runner class
            game = Blackjack()

            # create a deck object
            deck = Deck(1)
            
            # shuffle the deck
            deck.shuffle()
            
            while True:
                # bet
                game.bet(players)
                sleep(0.5)
                clear_screen()
                
                # deal the first four cards (alternating player/comp/player/comp)
                game.deal(deck, players)
                game.deal(deck, players)
                house.add_card(deck)
                
                game.print_hands(players, house)
                
                for player in players:
                    if player.hand.natural_blackjack:
                        print(f'\n{player.name} has gotten a natural black jack with {player.hand.cards}!')
                
                # let the player take their turn (meaning they can choose more cards until they choose to stop or bust)
                for player in players:
                    sleep(0.5)
                    game.player_turn(deck, player)
                    clear_screen()
                    game.print_hands(players, house)
                    
                clear_screen()
                game.house_turn(deck, house)
                
                print('')
                game.find_winner(players, house)
                
                if input("Continue? (y/n): ").lower() == 'n':
                    break
                else:
                    clear_screen()
                    for player in players:
                        player.hand.clear_cards()
                        house.clear_cards()
                
                
                # if the player's sum doesn't exactly equal to 21, let the computer take its turn (meaning it can choose more cards until it chooses to stop or bust)
                
                # calculate who the winner is

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    
# run the main program
if __name__ == '__main__':
    Blackjack().main()
