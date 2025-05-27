import redis
REDIS_CONFIG = {
    "host": "redis-13357.c92.us-east-1-3.ec2.redns.redis-cloud.com",
    "port": 13357,
    "decode_responses": True,
    "username": "default",
    "password": "MaMdTtfUFDj2vtOMjwD4IK3F2lae4oUP",
}

r= redis.Redis(**REDIS_CONFIG)
r.set("num", 35)