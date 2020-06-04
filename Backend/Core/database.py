import redis


class redisDB:
    redisHost = "localhost"
    redisDB = redis.Redis(host=redisHost, port=6379, db=0)

    def setData(self, data):
        # parse data to python Object
        with self.redisDB as DB:
            for i in range(len(data["data"])):
                name = data["requestname"] + ":" + data["data"][i]
                DB.set(name=name, value=data["data"][i])
                DB.expire(name=name, time=86400)
