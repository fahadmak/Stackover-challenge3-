
class User(object):
    def __init__(self, user_id, name, username, password):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password

class Question(object):
   
    def __init__(self, qn_id, title, body, user_id):
        self.qn_id = qn_id
        self.title = title
        self.body = body
        self.user_id = user_id
    

class Answer(object):

    def __init__(self, qn_id, an_id, descr, user_id):
        self.descr = descr
        self.qn_id = qn_id
        self.an_id = an_id
        self.user_id = user_id

