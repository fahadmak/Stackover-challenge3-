questions = []
answers = []

class Question(object):
   
    def __init__(self, qn_id, title, body):
        self.title = title
        self.qn_id = qn_id
        self.body = body
    
    def to_json(self):
        data = {'qn_id' : self.qn_id, 'title' : self.title, 'body' : self.body}
        return data

    @classmethod
    def create_question(cls, qn_id, title, body):
        question = Question(qn_id, title, body)
        questions.append(question)
        return True

    @classmethod
    def get_qn_byID(cls, qn_id):
        qn = []
        for question in questions:
            quest = question.to_json()            
            qn.append(quest)
        qid = [ques_id for ques_id in qn if ques_id['qn_id'] == qn_id]
        return qid
            
    @classmethod
    def get_all_questions(cls):
        quns =[]
        for question in questions:
            quest = question.to_json()            
            quns.append(quest)
            print(quns)
        return quns

class Answer(object):

    def __init__(self, qn_id, an_id, descr):
        self.descr = descr
        self.qn_id = qn_id
        self.an_id = an_id

    @classmethod
    def create_answer(cls, qn_id, an_id, descr):
        for question in questions:
            if question.qn_id == qn_id: 
                answer = Answer(qn_id, an_id, descr)
                answers.append(answer)
                return True

    def to_json(self):
        data = {'qn_id' : self.qn_id, 'an_id' : self.an_id, 'descr' : self.descr}
        return data

    @classmethod
    def get_all_answers(cls):
        ans =[]
        for answer in answers:
            answ = answer.to_json()            
            ans.append(answ)
        return ans

    # @classmethod
    # def get_an_byID(cls, qn_id):
    #     an = []
    #     for answer in answers:
    #         answer = answer.to_json()            
    #         an.append(answer)
    #     a_id = [ans_id for ans_id in an if ans_id['qn_id'] == qn_id]
    #     ans = a_id[-1]
    #     return ans