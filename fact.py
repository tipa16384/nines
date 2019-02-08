#!/usr/bin/python

# play = ai[(player,hand,board,move)] = matches

from itertools import permutations
from random import randint

matches = {}
startingMatches = 1
startingBoard = frozenset(range(1,10))
numGames = 100000

play = {}
players = range(2)
hands = [frozenset([]) for p in players]
playRecord = [[] for p in players]

human = False

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
	#if human:
	#	print "Player {} has hand {}".format(player, newHand)
	return frozenset(newHand), frozenset(newBoard)

def winningHand(hand):
	if len(hand) < 3:
		return False
	for p in permutations(hand, 3):
		if sum(p) == 15:
			#print "{} is a winning hand".format(hand)
			return True
	return False

def choosePlay(player, hand, plays):
	if human:
		print "Player {} has this hand {} and these plays {}".format(player, list(hands[player]), plays.keys())
	if not human:
		for p in plays:
			nh = list(hand)
			nh.append(p)
			if winningHand(nh):
				return p
		tots = sum(plays.values())
		ch = randint(0,tots)
		#print "Plays {} choice {}".format(plays, ch)
		for p in plays:
			ch -= plays[p]
			if ch <= 0:
				return p
		print "error in choosePlay"
		return plays[0]
	elif player == 1:
		best = max(plays.values())
		p = [p for p in plays if plays[p] == best][0]
		print "Computer chooses {}".format(p)
		return p
	else:
		p = int(raw_input("Your move: "))
		return p

def playGame(player, board):
	global playRecord
	if len(board) == 0:
		if human:
			print player, "No more moves"
		return -1
	hand = hands[player]
	plays = getPlays(player, hand, board)
	if human:
		print "Available plays: {}".format(plays)
	move = choosePlay(player, hand, plays)
	tup = tuple([player, hand, board, move])
	playRecord[player].append(tup)
	nh, nb = makePlay(player, hand, board, move)
	hands[player] = nh
	if winningHand(nh):
		if human:
			print "Player {} wins!".format(player)
		return player
	else:
		return playGame(1 - player, nb)	

for i in range(numGames):
	hands = [frozenset([]) for p in players]
	playRecord = [[] for p in players]
	player = playGame(0, startingBoard)
	if player == -1:
		for p in players:
			for rec in playRecord[player]:
				play[rec] += 1
	else:
		for rec in playRecord[player]:
			play[rec] += 10

print getPlays(0, frozenset([]), startingBoard)

human = True

while True:
	hands = [frozenset([]) for p in players]
	playRecord = [[] for p in players]
	player = playGame(0, startingBoard)
	for rec in playRecord[player]:
		play[rec] += 1
	print
	print
