#Logan Pinel
#Started: September 23, 2024
#Personal Project to try and use what I learned in the slotmachine tutorial to build
#a basic level blackjack game

#import modules
import random

#global constant for min and max bets
MAX_BET = 500
MIN_BET = 5
MIN_DEPOSIT = 5
#global constant for the players balance
BALANCE = 0

#create a list for the cards
list_of_cards = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

#deposit function to get the amount the user wants to deposit
def deposit():
    global BALANCE
    while True:
        amount = input("How much money would you like to depost? $")
        if amount.isdigit():
            amount = int(amount)
            #amount greater than 0
            if amount > MIN_DEPOSIT:
                break
            else:
                print("Amount must be greater than $5.")
        else:
            print("Please enter a number.")
    
    BALANCE += amount
    return amount

#get_bet function to get the users bet
def get_bet():
    global BALANCE
    while True:
        bet = input("How much would you like to bet? $")
        if bet.isdigit():
            bet = int(bet)
            #bet is greater than balance
            if bet > BALANCE:
                print("You dont have enough balance to bet that much.")
            #if bet is between the bounds break
            elif MIN_BET <= bet <= MAX_BET:
                break
            #if bet isnt between the bounds
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}")
        else:
            print("Please enter a number.")
    
    BALANCE -= bet
    return bet

#get_hand() function to get the first two cards of a hand #can be used for both player and dealer
def get_hand():
    hand = []
    card_value = 0
    #get two random cards and add them to the list
    for i in range(1, 3):
        hand.append(random.choice(list_of_cards))
    
    #calculate the total card value
    for value in range(len(hand)):
        card_value += int(hand[value])

    return hand, card_value

#dealer_hit() function will give the dealer more cards
#will be used inside the hit_or_stand() function if the player hits
def dealer_hit(dealerhand, dealertotal, bet):
    global BALANCE
    #dealer can only hit if hand is less that 17 total
    while dealertotal < 17:
        new_card = int(random.choice(list_of_cards))
        dealerhand.append(new_card)
        print("The dealer draws.")
        print(*dealerhand)
        dealertotal += new_card
        print(f"The dealer is now at {dealertotal}")
        #if the dealer busts player wins
        if dealertotal > 21:
            BALANCE += bet * 2
            print("The dealer busted. \nYou win!")
            print("You won $" + str(bet * 2))
            print("Balance: {}".format(BALANCE))
            break
        #if the dealer has 21 player loses
        elif dealertotal == 21:
            print("Dealer Wins.")
            print("You lost $" + str(bet))
            print("Balance: {}".format(BALANCE))
            break
    #return the dealers total so we can update it for comparison later
    return dealertotal

#hit_or_stand() function will determine if the player wants to hit or stand
def hit_or_stand(hand, total, dealerhand, dealertotal, bet):
    global BALANCE
    while True:
        decision = input("Would you like to \"Hit\" or \"Stand\"? ")
        if decision == "Hit":
            #deal a new card
            new_card = int(random.choice(list_of_cards))
            #add that card to players hand
            hand.append(new_card)
            print(*hand) #use splat operator to print out the list nicely
            total += new_card #increment the players total by the new_card value
            print(f"You are now at {total}")
            #does the player want to hit again use recursion to run the fucntion again
            if total < 21:
                hit_or_stand(hand, total, dealerhand, dealertotal, bet)
            #if the player busted tell them they lost
            elif total > 21:
                print("You busted.")
                print("You lost $" + str(bet))
            #if player has 21
            elif total == 21:
                BALANCE += bet * 2
                print("You win!")
                print("You won $" + str(bet * 2))
                print("Balance: {}".format(BALANCE))
            #break out of loop
            break
        elif decision == "Stand":
            print("You stand.")
            #set the new dealers total which is returned when calling dealer_hit()
            newdealertotal = dealer_hit(dealerhand, dealertotal, bet)
            #if dealer wins automatically
            if 21 > newdealertotal > total:
                print("Dealer Wins.")
                print("You lost $" + str(bet))
                print("Balance: {}".format(BALANCE))
            #if player stands
            elif newdealertotal < total:
                BALANCE += bet * 2
                print("You Win!")
                print("You won $" + str(bet * 2))
                print("Balance: {}".format(BALANCE))
            #if push
            elif newdealertotal == total:
                BALANCE += bet
                print("Push")
            #if the dealer busted update the players balance
            elif newdealertotal > 21:
                BALANCE += bet * 2
            break
        else:
            print("Please type \"Hit\" or \"Stand\"")

#def game() function to play the game
def game():
    #get the players bet
    bet = get_bet()
    #get the player and the dealers hands
    players_hand, player_card_value = get_hand()
    dealers_hand, dealer_card_value = get_hand()
    #print out the users hand and the total value
    print(*players_hand) #use splat operator to print out the list nicely
    print(f"You are at {player_card_value}")
    #print out the dealers hand and the total value
    print(*dealers_hand)
    print(f"The dealer is at {dealer_card_value}")
    #call the hit or stand method so game can progress
    hit_or_stand(players_hand, player_card_value, dealers_hand, dealer_card_value, bet)   

#main function()
def main():
    print("Welcome to Tampa Black Jack!")
    #get the players deposit
    deposit()
    #play again feature
    while True:
        game()
        play_again = input("Press enter to play again. Press \"q\" to quit. ")
        if play_again == "q":
            break
    #ending statement   
    print(f"You left with ${BALANCE}.")

#call main
main()