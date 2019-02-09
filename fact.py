#!/usr/bin/python

from itertools import permutations
from random import randint, choice
from threading import Thread
from time import sleep
import sys

startingMatches = 1
startingBoard = frozenset(range(1,10))
numGames = 100

class Player():
	__number__ = 0
	
	def __init__(self, name, human):
		self.name = name
		self.human = human
		self.id = Player.__number__
		Player.__number__ += 1
	
	def getId(self):
		return self.id
	
	def getName(self):
		return self.name
	
	def getHuman(self):
		return self.human

class AI(Thread):
	def __init__(self):
		super(AI, self).__init__(name = 'hello')
		self.stopMe = False
	
	def stop(self):
		self.stopMe = True
		print "Trying to stop"
	
	def run(self):
		global players, playRecord, play, playerNames, playerHuman
		print "I LIVE!"
		maxIQ = 100000
		count = 0
		
		while not self.stopMe and count < maxIQ:
			count += 1
			hands = [frozenset([]) for p in players]
			playRecord = [[] for p in players]
			player = playGame(True, players[0], startingBoard, hands)
			if player is None:
				for p in players:
					for rec in playRecord[p.getId()]:
						play[rec] += 1
			else:
				for p in players:
					for rec in playRecord[player.getId()]:
						play[rec] = (play[rec] + 10) if p == player else max(1, play[rec]-1)
		
		if count >= maxIQ:
			print
			print "(Yawn) I've learned all I can. You're on your own, now."
		else:
			print "Exiting!"

play = {}
xplayerNames = [ 'Earthling', 'Robot Overlord' ]
xplayerHuman = [ True, False ]

players = [Player('Earthling', True), Player('Robot Overlord', False)]
playRecord = [[] for p in players]
stopThread = False

brains = AI()
brains.start()

def nextPlayer(player):
	if player == players[0]:
		return players[1]
	return players[0]

def prettyList(l):
	a = list(l)
	a.sort()
	return ' '.join([str(x) for x in a]) if len(a) > 0 else 'No cards'

def getPlays(player, hand, board):
	#print "Player {} has hand {} board {}".format(player, hand, board)
	plays = {}
	for move in board:
		tup = tuple([player, hand, board, move])
		if tup not in play:
			play[tup] = startingMatches
		plays[move] = play[tup]
	return plays

def makePlay(player, hand, board, move):
	newHand = list(hand)
	newHand.append(move)
	newHand.sort()
	newBoard = list(board)
	newBoard.remove(move)
	return frozenset(newHand), frozenset(newBoard)

def winningHand(hand):
	if len(hand) < 3:
		return False
	for p in permutations(hand, 3):
		if sum(p) == 15:
			#print "{} is a winning hand".format(hand)
			return True
	return False

def choosePlay(learningMode, player, hand, plays, hands):
	global stopThread
	if learningMode:
		for p in plays:
			nh = list(hand)
			nh.append(p)
			if winningHand(nh):
				return p
		if randint(0,100) > 50:
			tots = sum(plays.values())
			ch = randint(0,tots)
			#print "Plays {} choice {}".format(plays, ch)
			for p in plays:
				ch -= plays[p]
				if ch <= 0:
					return p
		else:
			return choice(plays.keys())
		print "error in choosePlay"
		return plays[0]
	elif not player.getHuman():
		best = max(plays.values())
		p = [p for p in plays if plays[p] == best][0]
		print "{} chooses {}".format(player.getName(), p)
		return p
	else:
		you = nextPlayer(player)
		print "Available cards: {}".format(prettyList(plays.keys()))
		print "{}'s cards: {}".format(you.getName(), prettyList(hands[you.getId()]))
		print "Your cards: {}".format(prettyList(hands[player.getId()]))

		while True:
			p = raw_input("Your move, {} (Q to quit): ".format(player.getName()))
			if p in ['q','Q']:
				brains.stop()
				sys.exit(0)
			p = int(p)
			if p in plays:
				return p
			else:
				print "Invalid move"

def playGame(learningMode, player, board, hands):
	global playRecord
	if len(board) == 0:
		if not learningMode:
			print "DRAW!"
		return None
	hand = hands[player.getId()]
	plays = getPlays(player, hand, board)
	#if not learningMode and player.getHuman():
	#	print "Available plays: {}".format(plays)
	move = choosePlay(learningMode, player, hand, plays, hands)
	tup = tuple([player, hand, board, move])
	playRecord[player.getId()].append(tup)
	nh, nb = makePlay(player, hand, board, move)
	hands[player.getId()] = nh
	if winningHand(nh):
		if not learningMode:
			print "{} wins!".format(player.getName())
		return player
	else:
		return playGame(learningMode, nextPlayer(player), nb, hands)	

while True:
	hands = [frozenset([]) for p in players]
	playRecord = [[] for p in players]
	player = playGame(False, players[0], startingBoard, hands)
	if player:
		for rec in playRecord[player.getId()]:
			play[rec] += 1
	print
	print