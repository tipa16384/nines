#!/usr/bin/python

from itertools import permutations
from random import randint, choice
from threading import Thread
from time import sleep
import sys

startingMatches = 1
startingBoard = frozenset(range(1,10))
numGames = 100

play = {}
playerNames = [ 'Earthling', 'Robot Overlord' ]
playerHuman = [ True, False ]

players = range(len(playerNames))
playRecord = [[] for p in players]
stopThread = False

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
		count = 0
		
		while not self.stopMe:
			hands = [frozenset([]) for p in players]
			playRecord = [[] for p in players]
			player = playGame(True, 0, startingBoard, hands)
			if player == -1:
				for p in players:
					for rec in playRecord[player]:
						play[rec] += 1
			else:
				for p in players:
					for rec in playRecord[player]:
						play[rec] = (play[rec] + 10) if p == player else max(1, play[rec]-1)
		
		print "Exiting!"

brains = AI()
brains.start()

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
	elif not playerHuman[player]:
		best = max(plays.values())
		p = [p for p in plays if plays[p] == best][0]
		print "{} chooses {}".format(playerNames[player], p)
		return p
	else:
		print "{} has this hand {} and these plays {}".format(playerNames[player], list(hands[player]), plays.keys())
		while True:
			p = raw_input("Your move, {} (Q to quit): ".format(playerNames[player]))
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
		return -1
	hand = hands[player]
	plays = getPlays(player, hand, board)
	if not learningMode and playerHuman[player]:
		print "Available plays: {}".format(plays)
	move = choosePlay(learningMode, player, hand, plays, hands)
	tup = tuple([player, hand, board, move])
	playRecord[player].append(tup)
	nh, nb = makePlay(player, hand, board, move)
	hands[player] = nh
	if winningHand(nh):
		if not learningMode:
			print "{} wins!".format(playerNames[player])
		return player
	else:
		return playGame(learningMode, 1 - player, nb, hands)	

while True:
	hands = [frozenset([]) for p in players]
	playRecord = [[] for p in players]
	player = playGame(False, 0, startingBoard, hands)
	for rec in playRecord[player]:
		play[rec] += 1
	print
	print