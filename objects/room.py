from enum import Enum
import datetime
import random

class RoomState(Enum):
    gmae = 1
    bee = 2
    cat = 3
    dog = 4


class Record:
    def __init__(self, author, text):
        self.author = author
        self.text = text
        self.timestamp = datetime.datetime.now().strftime("%H:%M:%S")


class Room:
    def __init__(self, room_id, bet, user_id=None, user=None):
        self.player = []
        self.croupierCarts = []
        self.isFinishField = False
        self.carts = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4
        random.shuffle(self.carts)
        self.room_id = room_id
        self.user_id = None
        self.user = user
        self.records = []
        
        self.bid = bet

        self.StartGameOnePlayer()

    def check_auth(self, user_id):
        if self.user_id is None:
            return True
        return user_id == self.user_id

    def getCarts(self):
        for i in range(2):
            self.croupierCarts.append(self.carts.pop())
        for i in range(2):
            self.player.append(self.carts.pop())

    def getNextCartForPlayers(self, array, is_me=False):
        random.shuffle(self.carts)
        card = self.carts.pop()
        array.append(card)
        if is_me:
            self.records.append(Record('You', "You hit and get:" + card))

    def getScore(self, array):
        score = 0
        for cart in array:
            if cart == "J" or cart == "Q" or cart == "K":
                score += 10
            else:
                if cart == "A":
                    if score >= 11:
                        score += 1
                    else:
                        score += 11
                else:
                    score += int(cart)
        return score

    def printResults(self):
        result = ''
        result += "Dealaer carts: " + str(self.croupierCarts) + ". Total score: " + str(self.getScore(self.croupierCarts)) + "\n"
        result += "You carts:" + str(self.player) + ". Total score: " + str(self.getScore(self.player)) + "\n"
        return result

    def checkBlackjack(self):
        result = ''
        if self.getScore(self.player) == 21:
            result += "You are winner!!!"
            result += self.printResults()
            self.isFinishField = True
        if self.getScore(self.croupierCarts) == 21:
            result += "You lose: dieler win!!"
            result += self.printResults()
            self.isFinishField = True

        if result:
            self.records.append(Record('Game', result))

    def getResults(self):
        result = self.printResults()
        strBet = str(self.bid)
        if self.getScore(self.player) == 21:
            result += "You winner" + strBet + "!\n"
            self.user.balance += self.bid
        elif self.getScore(self.croupierCarts) == 21:
            result += "You lose" + strBet + "! You stupid! Dealer win!\n"
            self.user.balance -= self.bid
        elif self.getScore(self.player) > 21:
            result += "You lose" + strBet + "! Total score > 21!\n"
            self.user.balance -= self.bid
        elif self.getScore(self.croupierCarts) > 21:
            result += "You win" + strBet + "! Dealers total score > 21!\n "
            self.user.balance += self.bid
        elif self.getScore(self.player) < self.getScore(self.croupierCarts):
            result += "You lose" + strBet + "! Your score least than dealer score!\n"
            self.user.balance -= self.bid
        elif self.getScore(self.player) > self.getScore(self.croupierCarts):
            result += "You win" + strBet + "! Yout score is higher tha the dealers score!\n"
            self.user.balance += self.bid
        else:
            result += "You don't lose and don't win! Gool luck)\n!"
            self.user.balance += self.bid
        self.records.append(Record("Game", result))
        self.isFinishField = True
        return result

    def hit(self):
        self.getNextCartForPlayers(self.player, is_me=True)

        if self.getScore(self.player) > 21:
            self.getResults()
            return

        while self.getScore(self.croupierCarts) < 17:
            self.getNextCartForPlayers(self.croupierCarts, is_me=False)

    def stand(self):
        while self.getScore(self.croupierCarts) < 17:
            self.getNextCartForPlayers(self.croupierCarts)

        self.records.append(Record('You', "You stand"))

        self.getResults()

    def quit(self):
        while self.getScore(self.croupierCarts) < 17:
            self.getNextCartForPlayers(self.croupierCarts)
        self.getResults()

        self.records.append(Record('Сroupier', "Bye!"))

    def bet(self, bid):
        if self.user.balance < bid:
            self.records.append(Record('You', "You don't have so much money!!!!!"))
        else :
            self.bid += bid
            self.records.append(Record('You', "You bid increased by " + bid + "!"))

    def gameFinish(self):
        self.isFinishField = True

    def isFinish(self):
        return self.isFinishField

    def player_score(self):
        return str(self.getScore(self.player))

    def StartGameOnePlayer(self):
        self.records.append(Record('Сroupier', 'Welcome to blackjack!'))
        self.getCarts()
        self.records.append(Record('Сroupier', "Dieler is showing carts:" + str(self.croupierCarts[0])))

        self.checkBlackjack()

