import asyncio

class Server(object):
	Chats = set()
	Users = set()

	def __init__(self, loop=None):
		return 

	async def UserOnline(self, user=None):
		if user:
			self.Users.add(user)
			print(">>", self.Users)
		return

	async def UserOffline(self, user=None):
		if user:
			self.Users.remove(user)
		return

	# TODO: Implement Chat Sharding and Locking