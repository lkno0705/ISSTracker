import json

import redis


def process(data):
    __redisHost__ = ""
    __redisDB__ = redis.Redis(host=__redisHost__, port=6379, db=0, password="")
    astros = data['astros']
    for i in range(len(astros)):
        __redisDB__.set(name="Astronaut:" + astros[i]['name'] + ":picture", value=astros[i]['picture'])
        __redisDB__.set(name="Astronaut:" + astros[i]['name'] + ":nation", value=astros[i]['nation'])
        __redisDB__.set(name="Astronaut:" + astros[i]['name'] + ":flag", value=astros[i]['flag'])
        print("Astronaut:" + astros[i]['name'] + ": picture"+astros[i]['picture'])


file = open(r"astros_pics_flags_nations.json")
data = json.load(file)
process(data)
file.close()

