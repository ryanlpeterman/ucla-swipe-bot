from tinydb import TinyDB, Query
from util import log
from copy import deepcopy

# 2 possible is_buying
buying = [True, False]
# 4 possible dining halls
dining_halls = ["DENEVE", "BPLATE", "FEAST", "COVEL"]
# 6am - 9pm
times = range(6, 21)
# possible prices are up to $10
prices = range(10)

def init():
	"""
	builds the tree structure for all possible user fields
	"""
	# global tree structure
	global d

	# buying bottom level
	d = dict((x, []) for x in buying)

	# times bottom level
	d = dict((x, deepcopy(d)) for x in times)

	# adds prices as next top level
	# d = dict((x, d) for x in prices)

	# adds dining halls as top most level
	d = dict((x, deepcopy(d)) for x in dining_halls)

def add_complete_user(usr):
	"""
	adds a user dict in the following format and returns new matches if any
	format of usr:
	{
		halls: list of halls 'BPLATE', 'DENEVE',
		times: list of military times (ints),
		is_buyer: bool,
		id: int representing their uid
	}
	"""
	halls = usr["where"]
	times = usr["when"]
	is_buyer = usr["is_buyer"]
	uid = usr["id"]

	# list of uid pairs containing matches
	# uid1, uid2, hall, time
	matches = []

	for hall in halls:
		for time in times:
			node = d[hall][time][is_buyer]

			if uid not in node:
				d[hall][time][is_buyer].append(uid)

			# if seller of the same data but opposite buying status exists
			if d[hall][time][not is_buyer]:
				match = d[hall][time][not is_buyer]
				matches.append((match[0], uid, hall, time))

	return matches

if __name__ == '__main__':
	# example use case
	init()
	usr1 = {'id':1234, 'where':['BPLATE', 'DENEVE'], 'when':[8,9], 'is_buyer':False}
	print add_complete_user(usr1)
	usr2 = {'id':6969, 'where':['BPLATE', 'DENEVE'], 'when':[8,9], 'is_buyer':True}
	print add_complete_user(usr2)