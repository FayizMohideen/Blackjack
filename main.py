import random
import discord
import json
import os
from uptime import keep_alive

#Starting by building the deck of cards
class Card(object):
  def __init__(self,suit,value):
    self.suit = suit
    self.value = value
  def form(self):
    print ('%s%s' % (self.value, self.suit))

#unicode suits
unisuits = {'spades': '\u2664', 'hearts' : '\u2661','diamonds' : '\u2662', 'clubs' : '\u2667'  }

values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']


#fdeck stands for formatted deck
class Deck(Card):
  
  def __init__(self):
    self.cards = []
    self.fdeck = []
    self.player_hand = []
    self.dealer_hand = []
  
  def makedeck(self):
    for suit in unisuits:
      for value in values:
        self.cards.append(Card(unisuits[suit],value))
  
  def form(self):
    for x in self.cards:
      self.fdeck.append('%s%s' % (x.value, x.suit))
  
  def dealerdeal(self,n):
    for x in range(n):
      self.dealer_hand.append(self.fdeck[x])
      del(self.fdeck[x])
      random.shuffle(self.fdeck)
    print ('Dealer hand: ' +' | '.join(self.dealer_hand))
    print ('Dealer Value: ' + str(self.dvalue()))
   
  def playerdeal(self,n):
    for x in range(n):
      self.player_hand.append(self.fdeck[x])
      del(self.fdeck[x])
      random.shuffle(self.fdeck)
    print ('Player hand: ' + ' | '.join(self.player_hand))
    print ('Player Value: ' + str(self.pvalue()))
  
  def totalvalue(self,list):
    valuetotal = 0
    for card in list:
      value = card[0]
      if value != 'A':
        valuetotal += cvalues[value]
      else:
        if valuetotal + 11 >21:
          valuetotal += 1
        else: valuetotal += 11  
    return valuetotal

  def pvalue(self): 
    return self.totalvalue(self.player_hand)

  def dvalue(self):
    return int(self.totalvalue(self.dealer_hand))

#Setting up the counter
#values except Ace
cvalues = {'2':2,'3':3, '4':4,'5': 5,'6': 6, '7':7,'8':8,'9':9,'1':10, 'J':10,'Q':10,'K':10}


class Game(Deck):
  def __init__(self, bet):
    self.deck = Deck()
    self.deck.makedeck()
    for x in range(5):
      random.shuffle(self.deck.cards)
    self.deck.form()
    self.deck.dealerdeal(1)
    self.deck.playerdeal(2)
    self.player_bust = False
    self.dealer_bust = False
    self.player_stand = False
    self.dealer_stand = False
    self.player_blackjack = False
    self.dealer_blackjack = False
    self.bet = bet
    self.hit = 0
  

  def playerbust(self):
    if self.deck.pvalue() > 21:
      self.player_bust = True


  def dealerbust(self):
    if self.deck.dvalue() > 21:
      self.dealer_bust = True

  def playerblackjack(self):
    if self.deck.pvalue() == 21:
      self.player_blackjack = True

  def dealerblackjack(self):
    if self.deck.dvalue() == 21:
      self.dealer_blackjack = True

  def win_check(self):
    if self.dealer_bust == True:
      if self.player_bust == True:
        return 'BB' # return BB
      elif self.player_bust == False:
        return 'DB' #return DB
    else:
      if self.player_bust == True:
        return 'PB' #return PB
      else:
        if self.player_stand == True and self.dealer_stand == True:  
          if self.dealer_blackjack == False and self.deck.dvalue() > self.deck.pvalue():
            return 'DH'
          elif self.dealer_blackjack == True and self.deck.dvalue() > self.deck.pvalue():
            return 'DBL'
          elif self.player_blackjack == False and self.deck.pvalue() > self.deck.dvalue():
            return 'PH'
          elif self.player_blackjack == True and self.deck.pvalue() > self.deck.dvalue():
            return 'PBL'
          elif self.player_blackjack == False and self.deck.pvalue() == self.deck.dvalue():
            return 'T'
          elif self.player_blackjack == True and self.deck.pvalue() == self.deck.dvalue():
            return 'TBL'
            
  def play(self,action):
    if action == 'hit':
      self.deck.playerdeal(1)
      if self.deck.dvalue() < 17:
        self.deck.dealerdeal(1)
      else: self.dealer_stand = True
      self.hit = 1
    if action == 'double':
      if self.hit == 0:
        self.bet = 2 * self.bet
      self.deck.playerdeal(1)
      if self.deck.dvalue() < 17:
        self.deck.dealerdeal(1)
      else: self.dealer_stand = True
      self.hit = 1

    elif action == 'stand':
      self.player_stand = True
      while self.deck.dvalue() < 17:
        self.deck.dealerdeal(1)
      else: self.dealer_stand = True
      if self.deck.pvalue() < 21:
        if self.deck.pvalue() > self.deck.dvalue():
          self.deck.dealerdeal(1)
        else: self.dealer_stand = True

    self.playerblackjack()
    self.dealerblackjack()
    self.playerbust()
    self.dealerbust()


client = discord.Client()
client.games = {}
player_bets = {}


with open('scoreboard.json') as save_file:
  player_bets = json.load(save_file)
  save_file.close()

@client.event
async def on_ready():
  print('I am {0.user}'.format(client))

@client.event
async def on_message(message):

  if message.content.startswith('$Timetable') or message.content.startswith('$timetable'):
    embedVar = discord.Embed(title = 'Timetable', description = '{}\'s Timetable'.format(message.author.name))
    if message.author.name == 'LISE':
      embedVar.add_field(name = 'Sunday', value = 'Accounting\n Free \n Free \n Chemistry \n Maths \n Physics', inline = True)
      embedVar.add_field(name = 'Monday', value = 'Chemistry \n Accounting \n Maths \n Physics \n Free \n Free', inline = True)
      embedVar.add_field(name = 'Tuesday', value = 'Physics \n Accounting \n Free \n Free \n Chemistry \n Maths', inline = True)
      embedVar.add_field(name = 'Wednesday' , value = 'Physics \n Free \n Free \n Accounting \n Chemistry \n Maths', inline = True)
      embedVar.add_field(name = 'Thursday' , value = 'Free \n Maths \n Physics \n Free \n Accounting \n Chemistry', inline = True)
    embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$blj play'):
    # giving the player an initial wallet of 100 or if they're broke
    if message.author.name not in player_bets:
      player_bets[message.author.name] = 100
      
    if player_bets[message.author.name] == 0:
      player_bets[message.author.name] = 100
    bet = int(message.content.split('$blj play',1)[1])
    # if they dont have enough, no game
    if player_bets[message.author.name] < bet:
      await message.channel.send('Bet less than ' + str(player_bets[message.author.name]))
      return
    # if they already have a game, no new game
    if message.author.name in client.games:
      await message.channel.send('You already have a game in progress.')
      return
    else: 
      player_bets[message.author.name] -= bet
      client.games[message.author.name] = Game(bet) 
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand)+'\n'+ 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
        
     
  elif message.content.startswith('$blj hit'):

    if message.author.name not in client.games:
      await message.channel.send('You don\'t have a game in progress.')
      return
      
    client.games[message.author.name].play('hit')

    embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
    embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
    embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
    embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
    await message.channel.send(embed=embedVar)

    if client.games[message.author.name].win_check() == 'BB':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You both bust!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
    
    elif client.games[message.author.name].win_check() == 'DB':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Dealer bust: You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'PB':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You bust!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
  
    elif client.games[message.author.name].win_check() == 'DH':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You lose!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

      
    elif client.games[message.author.name].win_check() == 'DBL':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Dealer blackjack: You lose!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
      
    elif client.games[message.author.name].win_check() == 'PH':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'PBL':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Blackjack: You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'T':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You Tied!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'TBL':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Double Blackjack: Tie!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

  elif message.content.startswith('$blj double'):

    if message.author.name not in client.games:
      await message.channel.send('You don\'t have a game in progress.')
      return
    if client.games[message.author.name].hit == 1:
      await message.channel.send('You\'ve already hit!')
      return

    client.games[message.author.name].play('double')
    

    embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
    embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
    embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
    embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
    await message.channel.send(embed=embedVar)

    if client.games[message.author.name].win_check() == 'BB':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You both bust!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
    
    elif client.games[message.author.name].win_check() == 'DB':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Dealer bust: You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'PB':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You bust!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'DH':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You lose!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

      
    elif client.games[message.author.name].win_check() == 'DBL':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Dealer blackjack: You lose!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
      
    elif client.games[message.author.name].win_check() == 'PH':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'PBL':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Blackjack: You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'T':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You Tied!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'TBL':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Double Blackjack: Tie!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()


  elif message.content.startswith('$blj stand'):
    
    if message.author.name not in client.games:
      await message.channel.send('You don\'t have a game in progress.')
      return
    
    client.games[message.author.name].play('stand')

    if client.games[message.author.name].win_check() == 'BB':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You both bust!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
    
    elif client.games[message.author.name].win_check() == 'DB':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Dealer bust: You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'PB':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You bust!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
  
    elif client.games[message.author.name].win_check() == 'DH':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You lose!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
      
    elif client.games[message.author.name].win_check() == 'DBL':
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Dealer blackjack: You lose!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()
      
    elif client.games[message.author.name].win_check() == 'PH':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'PBL':
      player_bets[message.author.name] += 2 * client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Blackjack: You Win!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])

      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'T':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'You Tied!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)
      
      del(client.games[message.author.name])
      
      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()

    elif client.games[message.author.name].win_check() == 'TBL':
      player_bets[message.author.name] += client.games[message.author.name].bet
      embedVar = discord.Embed(title='Blackjack', description ='{}\'s game of Blackjack'.format(message.author.name))
      embedVar.add_field(name='Dealer\'s hand', value = ' | '.join(client.games[message.author.name].deck.dealer_hand) + '\n' + 'Dealer Hand Value: ' + str(client.games[message.author.name].deck.dvalue()))
      embedVar.add_field(name='{}\'s hand'.format(message.author.name), value = ' | '.join(client.games[message.author.name].deck.player_hand)+ '\n' + 'Player Hand Value: ' + str(client.games[message.author.name].deck.pvalue()))
      embedVar.add_field(name = 'Double Blackjack: Tie!', value ='You now have ' + str(player_bets[message.author.name]) + ' chips in your wallet.', inline = False)
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed=embedVar)

      del(client.games[message.author.name])

      with open('scoreboard.json', 'w') as save_file:
        save_file.write(json.dumps(player_bets))
        save_file.close()



  elif message.content.startswith('$blj wallet'):

    embedVar = discord.Embed(title = '{}\'s Wallet'.format(message.author.name), description = 'You have ' + str(player_bets[message.author.name]) + ' chips')
    await message.channel.send(embed = embedVar)

  elif message.content.startswith('$blj help'):
    embedVar = discord.Embed(title = 'Blackjack Bot', description = 'List of Commands')
    embedVar.add_field(name = '$blj help', value = 'Displays a list of Blackjack Bot\'s commands', inline = False)
    embedVar.add_field(name = '$blj play <bet value>', value = 'Starts a game of Blackjack', inline = False)
    embedVar.add_field(name = '$blj hit', value = '$blj hit allows you to draw a card from the deck and add it to your hand', inline = False)
    embedVar.add_field(name = '$blj stand', value = 'Lets you stop drawing cards', inline = False)
    embedVar.add_field(name = '$blj double', value = 'A variation of hit which allows you to double your bet; Only works if you haven\'t hit yet')
    embedVar.add_field(name = '$blj wallet', value = 'Lets you check your chip count', inline = False)
    embedVar.add_field(name = '$blj scoreboard', value ='Displays the scoreboard',inline = False)
    embedVar.add_field(name ='$coinflip',value = 'Unsure what to do? Flip a coin!', inline = False)
    embedVar.add_field(name = 'The rules', value = 'The aim of the game is to keep drawing cards to get the highest total without going over 21.')
    embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
    await message.channel.send(embed = embedVar)

  elif message.content.startswith('!ping'):
    await message.channel.send('Pong!')

  elif message.content.startswith('$coinflip'):
    result= random.randint(0,1)
    pass
    if result == 0:
      embedVar = discord.Embed(title = 'Coinflip')
      embedVar.set_image(url='https://media.discordapp.net/attachments/745121929924575282/791380116760428554/heads.gif')
      await message.channel.send(embed = embedVar)
    elif result == 1:
      embedVar = discord.Embed(title = 'Coinflip')
      embedVar.set_image(url='https://cdn.discordapp.com/attachments/745121929924575282/791380117456814181/tails.gif')
      embedVar.set_footer(text= message.author.name, icon_url = message.author.avatar_url)
      await message.channel.send(embed = embedVar)

  elif message.content.startswith('$blj scoreboard'):
    embedVar = discord.Embed(title = 'Scoreboard')

    sort = sorted(player_bets.items(), key=lambda x: x[1], reverse=True)

    embedVar.add_field(name = ':crown: ' + str(sort[0][0]) + ' :crown:', value = str(sort[0][1]))

    sort.pop(0)

    for item in sort:
      embedVar.add_field(name = str(item[0]), value = str(item[1]), inline = False)

    await message.channel.send(embed = embedVar)
    
    
    

keep_alive()
client.run(os.getenv('Token'))

