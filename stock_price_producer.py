import math
import time
import json

import redis

REDIS_HOST_IP = "192.168.59.103"


def produce_forever():
    r_server = redis.Redis(REDIS_HOST_IP)
    while True:
        x = time.time()
        y = 2.5 * (1 + math.sin(x / 50))
        print "publish to channel metricA..."
        r_server.publish("metricA", json.dumps(dict(x=x, y=y)))
        print "publish to channel metricB..."
        r_server.publish("metricB", json.dumps(dict(x=x, y=2*y)))
        time.sleep(1)


if __name__ == "__main__":
    produce_forever()