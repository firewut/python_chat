class UserAlreadyExists(Exception):
    def __init__(self):
	    Exception.__init__(self,"User already exists")

class UserDoesNotExist(Exception):
	def __init__(self):
	    Exception.__init__(self,"User does not exist")	

class ChatWithMembersAlreadyExists(Exception):
	def __init__(self):
	    Exception.__init__(self,"Chat with these members already exists")

class ChatMembersRequired(Exception):
	def __init__(self):
	    Exception.__init__(self,"Chat Members are required")

