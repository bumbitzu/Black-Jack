import random
import time
import json

working_dir = 'Projects/BlackJack/'


def red(string):
    string = str(string)
    return '\033[1;31m' + string + '\033[0m'
def green(string):
    string = str(string)
    return '\033[1;32;40m' + string + '\033[0m'
def yellow(string):
    string = str(string)
    return '\033[1;33;40m' + string + '\033[0m'
def blue(string):
    string = str(string)
    return '\033[1;34;40m' + string + '\033[0m'
def purple(string):
    string = str(string)
    return '\033[1;35;40m' + string + '\033[0m'
def cyan(string):
    string = str(string)
    return '\033[1;36;40m' + string + '\033[0m'
def purple_back(string):
    string = str(string)
    return '\033[1;35;47m' + string + '\033[0m'
def red_white(string):
    string = str(string)
    return '\033[1;31;47m' + string + '\033[0m'
def black_white(string):
    string = str(string)
    return '\033[1;30;47m' + string + '\033[0m'
def black_black(string):
    string = str(string)
    return '\033[1;30;40m' + string + '\033[0m'
class BlackJack:
    
    def __init__(self, bet ):
        self.bet = bet
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.dealer_score = 0
        self.player_bust = False
        self.dealer_bust = False
        self.game_over = False
        self.winner = None
        self.player_turn = True
        self.dealer_turn = False
        self.player_stands = False
        self.dealer_stands = False
        self.player_blackjack = False
        self.dealer_blackjack = False
        self.player_ace = False
        self.dealer_ace = False
        self.player_ace_count = 0
        self.dealer_ace_count = 0
        self.cheat_on = False
        
    def create_deck(self):
        suits = ['\u2665', '\u2666', '\u2663', '\u2660']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for suit in suits:
            for value in values:
                self.deck.append((value, suit))
        
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def deal_cards(self):
        if self.cheat_on:
            self.player_hand.append(('A', 'Hearts'))
            self.dealer_hand.append(self.deck.pop())
            for card in self.deck:
                if card[0] == '10':
                    self.player_hand.append(card)
                    self.deck.remove(card)
                    break
            self.dealer_hand.append(self.deck.pop())
            return
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
        self.player_hand.append(self.deck.pop())
        self.dealer_hand.append(self.deck.pop())
    
    def calculate_score(self):
        self.player_score = 0
        self.dealer_score = 0
        self.player_ace_count = 0
        self.dealer_ace_count = 0
        for card in self.player_hand:
            if card[0] == 'J' or card[0] == 'Q' or card[0] == 'K':
                self.player_score += 10
            elif card[0] == 'A':
                self.player_score += 11
                self.player_ace_count += 1
            else:
                self.player_score += int(card[0])
        for card in self.dealer_hand:
            if card[0] == 'J' or card[0] == 'Q' or card[0] == 'K':
                self.dealer_score += 10
            elif card[0] == 'A':
                self.dealer_score += 11
                self.dealer_ace_count += 1
            else:
                self.dealer_score += int(card[0])
        while self.player_score > 21 and self.player_ace_count > 0:
            self.player_score -= 10
            self.player_ace_count -= 1
        while self.dealer_score > 21 and self.dealer_ace_count > 0:
            self.dealer_score -= 10
            self.dealer_ace_count -= 1
        if self.player_score == 21 and len(self.player_hand) == 2:
            self.player_blackjack = True
        if self.dealer_score == 21 and len(self.dealer_hand) == 2:
            self.dealer_blackjack = True
        if self.player_score > 21:
            self.player_bust = True
        if self.dealer_score > 21:
            self.dealer_bust = True
        if self.player_score == 21:
            self.player_stands = True
        if self.dealer_score == 21:
            self.dealer_stands = True
        if self.player_stands and self.dealer_stands:
            self.game_over = True
            if self.player_score > self.dealer_score:
                self.winner = 'Player'
            elif self.player_score < self.dealer_score:
                self.winner = 'Dealer'
            else:
                self.winner = 'Tie'
        if self.player_bust:
            self.game_over = True
            self.winner = 'Dealer'
        if self.dealer_bust:

            self.winner = 'Player'
    
    def player_hit(self):
        self.player_hand.append(self.deck.pop())
        self.calculate_score()
    
    def player_stand(self):
        self.player_stands = True
        self.player_turn = False
        self.dealer_turn = True
    
    def dealer_hit(self):
        if self.dealer_score < 17:
            self.dealer_hand.append(self.deck.pop())
            self.calculate_score()
        else:
            self.dealer_stands = True
            self.dealer_turn = False
            self.calculate_score()
    
    def play_game(self):
        input(f'Press {yellow("ENTER")} for new bet -> ')
        if self.no_enought_cash():
            return
        balance = Balance()
        balance.remove_cash(self.bet)
        balance.save_cash()
        
        self.create_deck()
        self.shuffle_deck()
        self.deal_cards()
        self.calculate_score()
        print(f"\n|{black_white("################ New Game ################ ")}|")
        while not self.game_over:
            if self.player_turn:
                print(f"{cyan('_____________________________')}")
                print(f'{cyan("********* Your Turn *********")}\n')
                print(f'{cyan("Your balance is: ")}{yellow('$')}{yellow(balance.get_balance())}\n')
                print(f'{cyan('Your Hand:')}',  self.paint_player_cards(self.player_hand))
                print(f'{cyan("Your Score:")} {yellow(self.player_score)}')
                print(f'{purple("Dealer Hand:")}',  self.paint_dealer_cards(self.dealer_hand))
                print('--------------------------------')
                action = input(f'Do you want to {yellow('hit')} or {green('stand')} ? -> ')
                if action == 'hit':
                    self.player_hit()
                elif action == 'stand':
                    self.player_stand()
                
            
            if self.dealer_turn:
                print(purple("_________________________________"))
                print(purple("********* Dealer's Turn *********\n"))
                print('Dealer is thinking...')
                if self.winner == None:
                    time.sleep(2)
                print(cyan('Your Hand:'), self.paint_player_cards(self.player_hand))
                print(f'{cyan("Your Score:")} {yellow(self.player_score)}')
                print(purple("Dealer Hand:"),  self.paint_dealer_cards(self.dealer_hand))
                print(purple('Dealer Score:'), yellow(self.dealer_score))
                print('--------------------------------')
                self.dealer_hit()
            
            
        
        if self.player_bust:
            print(f"{cyan('_____________________________')}")
            print(f'{cyan("********* Your Turn *********")}\n')
            print(f'{cyan("Your balance is: ")}{yellow('$')}{yellow(balance.get_balance())}\n')
            print(f'{cyan('Your Hand:')}',  self.paint_player_cards(self.player_hand))
            print(f'{cyan("Your Score:")} {yellow(self.player_score)}')
            print(f'{purple("Dealer Hand:")}',  self.paint_dealer_cards(self.dealer_hand))
            print('--------------------------------')
            print(red('<><><><><><><><><><><>'))
            print(red('<> You have busted! <>'))
            print(red('<><><><><><><><><><><>'))
        if self.dealer_bust:
            print(red('<><><><><><><><><><><><>'))
            print(red('<> Dealer has busted! <>'))
            print(red('<><><><><><><><><><><><>'))

        if self.winner == 'Player':
            print(green('****************'))
            print(green('*** You Win! ***'))
            print(green('****************'))
            balance = Balance()
            balance.add_cash(self.bet*2)
            balance.save_cash()
            print(f'{cyan("Your balance is: ")}{yellow('$')}{yellow(balance.get_balance())}\n')

        elif self.winner == 'Dealer':
            print(yellow('********************'))
            print(yellow('*** Dealer Wins! ***'))
            print(yellow('********************'))
        else:
            print(yellow('============='))
            print(cyan('= Tie Game! ='))
            print(yellow('============='))
            balance = Balance()
            balance.add_cash(self.bet)
            balance.save_cash()
            

        

    def no_enought_cash(self):
        balance = Balance()
        if balance.get_balance() < self.bet:
            return True
        else:
            return False
    def paint_player_cards(self, deck):
        string_deck = ''
        for card in deck:
            s_card = f'|{card[0]}{card[1]}|'

            if card[1] == '\u2665' or card[1] == '\u2666':
                string_deck+=(f'{red_white(s_card)},')
            else:
                string_deck+=(f'{black_white(s_card)},')
            
        return(string_deck)
    
    def paint_dealer_cards(self, deck):
        string_deck = ''
        if not self.player_turn:
            for card in deck:
                s_card = f'|{card[0]}{card[1]}|'
                if card[1] == '\u2665' or card[1] == '\u2666':
                    string_deck+=(f'{red_white(s_card)},')
                else:
                    string_deck+=(f'{black_white(s_card)},')
        else:
            for card in deck[:-1]:
                s_card = f'|{card[0]}{card[1]}|'
                if card[1] == '\u2665' or card[1] == '\u2666':
                    string_deck+=(f'{red_white(s_card)},')
                else:
                    string_deck+=(f'{black_white(s_card)},')
            
        return(string_deck)
    def turn_cheat_on(self):
        self.cheat_on = True
class PlayBlackJack:
    def __init__(self, number_of_games=1):
        self.number_of_games = number_of_games
    def play_game(self, cheat=None):
        bet = None
        try:
            bet = int(input('Enter your bet amount -> '))
        except:
            print('Invalid input! Please enter a valid amount.')
            #go back to the start of the function
            self.play_game()
        
        for i in range(self.number_of_games):
            game = BlackJack(bet)
            if cheat == 'cheat':
                game.turn_cheat_on()
            if game.no_enought_cash():
                print('You do not have enough cash to play the game!')
                break
            game.play_game()
class Balance:
    def __init__(self):
        with open(working_dir + 'cash.json', 'r') as file:
            data = json.load(file)
        self.cash = data['cash']
    def save_cash(self):
        data = {'cash': self.cash}
        with open(working_dir + 'cash.json', 'w') as file:
            json.dump(data, file)
    def add_cash(self, amount):
        self.cash += amount
    def remove_cash(self, amount):
        self.cash -= amount
    def get_balance(self):
        return self.cash