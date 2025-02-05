#Logan Pinel
#Started February 4th, 2025
#Basic text-based blackjack game that allows players to deposit a balance, place bets and play against the computer
#this project is made with a focus on object oriented programming
#FEATURES STILL WANTING TO IMPLEMENT:
    #double down
    #split
    #dealer showing only one card at start
    #potentially making a gui later on once i learn basic gui development in my CSC 102 class

#import modules
import random

#global constant for min and max bets
MAX_BET = 500
MIN_BET = 5
MIN_DEPOSIT = 5
#create a list for the deck of cards
deck_of_cards = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

#Player class which will handle all functions for the player
#this includes: 
class Player:
    #constructor
    def __init__(self, name):
        self.name = name
        #in addition to the parameter we need to initialize the players 
        #balance, hand, total card value, and their bet
        self.balance = 0
        self.hand = []
        self.totalValue = 0
        self.bet = 0

    #getter / setter methods for player name
    def getName(self):
        return self.name
    def setName(self, name):
        self.name = name

    #deposit method which will allow the player to deposit their money
    def deposit(self):
        #infinite loop to ensure the player enters a valid amount
        while True:
            #input the player
            amount = input("How much money would you like to depost? $")
            #check if the amount is a valid digit
            if amount.isdigit():
                #cast as int
                amount = int(amount)
                #amount greater than 0
                if amount >= MIN_DEPOSIT:
                    self.balance += amount
                    break
                else:
                    print("Amount must be greater than $5.")
            else:
                print("Please enter a number.")

    #placeBet method which will allow the player to place their bet
    def placeBet(self):
        #infinite loop to ensure the player enters a valid bet
        while True:
            #input the player
            bet = input("How much would you like to bet? $")
            #check if the bet is a valid digit
            if bet.isdigit():
                #cast as int
                bet = int(bet)
                #bet is greater than balance
                if bet > self.balance:
                    print("You dont have enough balance to bet that much.")
                #if bet is between the bounds break
                #VALID BET
                elif MIN_BET <= bet <= MAX_BET:
                    #subtract the bet from players balance and return the bet
                    self.balance -= bet
                    #update the players bet amount
                    self.bet = bet
                    #return the bet to break the loop
                    return bet
                #if bet isnt between the bounds
                else:
                    print(f"Amount must be between ${MIN_BET} - ${MAX_BET}")

    #drawCard method will draw cards to the players hand
    def drawCard(self):
        #draw a random card from the deck
        card = random.choice(deck_of_cards)
        #append the card to the players hand
        self.hand.append(card)
        #add the card value to the players total
        self.totalValue += int(card)

    #resetHand method will reset the players hand after each game is complete
    def resetHand(self):
        #reset the hand and totalValue to empty/zero
        self.hand = []
        self.totalValue = 0

    #winningHand method will modify the players balance if they win
    def winningHand(self):
        #update the players balance since they won a hand
        self.balance += (self.bet * 2)
        #print a message stating that the player won
        print("Player Wins!")
        #print out how much the player won
        print("You won: ${}".format(str(self.bet * 2)))
        #print out the players updated balance
        print("Balance: ${}".format(self.balance))


#Dealer class which will handle all functions for the dealer
#this class extends the Player class and inherits the drawCard and resetHand methods to limit duplicated code
class Dealer(Player):
    #constructor
    def __init__(self):
        #initialize the dealers hand a totalValue
        self.hand = []
        self.totalValue = 0

    #in blackjack dealers need to hit untill they have a toal card value of 
    #17 or greater
    #dealerTurn method will handle this function
    def dealerTurn(self):
        #infinite loop to check if the dealers totalValue >= 17
        while self.totalValue < 17:
            #print out a line to make the game easier to read for the player
            print("-" * 25)
            #call draw card and print a message
            self.drawCard()
            print("The dealer draws a card.")
            #print the dealers new hand
            print(f"Dealer Hand: {self.hand}")
        #print the dealers new total
        print(f"The dealer is now at {self.totalValue}")

#class for the game itself
class BlackJackGame:
    #contructor
    def __init__(self):
        #initialize the player
        self.player = Player(input("Please enter your name: "))
        #initialize the dealer
        self.dealer = Dealer()

    #playRound method that will handle the main game features
    def playRound(self):
        #get the players bet
        bet = self.player.placeBet()
        #create the hands using resetHand
        self.player.resetHand()
        self.dealer.resetHand()
        #now draw 2 cards for the player and dealer
        #can use a for loop with _ to just get 2 cards added
        for _ in range(2):
            self.player.drawCard()
            self.dealer.drawCard()
        #now print out the player and dealer hands
        print(f"Player Hand: {self.player.hand} | Value = {self.player.totalValue}")
        print(f"Dealer Hand: {self.dealer.hand} | Value = {self.dealer.totalValue}")

        #print out a line to make the game easier to read for the player
        print("-" * 25)

        #players turn
        #first check if the player got a black jack
        if self.player.totalValue == 21:
            #call winning hand method
            self.player.winningHand()
        #while loop to allow the player to hit or stand
        while self.player.totalValue < 21:
            playerDecision = input("Would you like to \"Hit\" or \"Stand\"? ").lower()
            #if the player chose to hit
            if playerDecision == "hit":
                #draw another card
                self.player.drawCard()
                #print out the players new hand and total
                print(f"Player Hand: {self.player.hand} | Value = {self.player.totalValue}")
                #check if the players new total is greater than 21
                if self.player.totalValue > 21:
                    print("Bust! Player Loses.")
                    #return to end the game
                    return
            #if the player stands
            else:
                #break out of the loop
                break

        #print out a line to make the game easier to read for the player
        print("-" * 25)

        #dealers turn
        #call the dealers dealerTurn method
        self.dealer.dealerTurn()

        #now determine who won
        #check if the dealer busted or if the players totalValue is greater than the dealers
        if (self.dealer.totalValue > 21) or (self.player.totalValue > self.dealer.totalValue):
            #the player wins so call the players winningHand method
            self.player.winningHand()
        #elif the player lost
        elif (self.player.totalValue < self.dealer.totalValue):
            #tell the player that they lost
            print(f"Dealer wins! You lost ${bet}. Balance: ${self.player.balance}")
        #anything else should be a push
        else:
            #give the player back their bet
            self.player.balance += bet
            #print out the push
            print("Push! Balance: ${self.player.balance}")

    #method to start the game
    def startGame(self):
        #print a welcome message
        print("Welcome to Tampa Black Jack!")
        #call the deposit method for the player so they can deposit money
        self.player.deposit()
        #infinite loop so that the game is played untill the player quits
        while True:
            #play a round
            self.playRound()
            #check if the player wants to quit
            if input("Press enter to play again | Press \"q\" to quit. ").lower() == "q":
                #break the loop to end the program
                break
        #if the loop is broken print a final message to show how much the player left with
        #print out a line to make the game easier to read for the player
        print("-" * 25)
        #final message
        print(f"You left with ${self.player.balance}.")

#MAIN PROGRAM
#initialize the game
game = BlackJackGame()
#start the game
game.startGame()
