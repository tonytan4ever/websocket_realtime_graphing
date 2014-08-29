import math
import time
import json

import redis

REDIS_HOST_IP = "<your_redis_ip>"


def produce_forever():
    r_server = redis.Redis(REDIS_HOST_IP)
    while True:
        x = time.time()
        y = 2.5 * (1 + math.sin(x / 50))
        print "publish to channel dataStreamA..."
        r_server.publish("dataStreamA", json.dumps(dict(x=x, y=y)))
        print "publish to channel dataStreamB..."
        r_server.publish("dataStreamB", json.dumps(dict(x=x, y=2*y)))
        time.sleep(1)


if __name__ == "__main__":
    produce_forever()