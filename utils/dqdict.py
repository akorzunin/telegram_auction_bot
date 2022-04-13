import json
class Dqdict(dict):
    '''Double quotes dictionary'''
    def __str__(self):
        return json.dumps(self)