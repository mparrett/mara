import redis
import sys

# http://redis.io/commands/rpoplpush

r = redis.StrictRedis(host='127.0.0.1', port=6379, password="secret")

if len(sys.argv) < 2:
    print("Please provide task")
    sys.exit(1)

worker_id = 1
processing_queue = str(worker_id) + '-queue'
work_queue = 'work'

fake_task = ' '.join(sys.argv[1:])
ret = r.lpush(work_queue, fake_task)

print('task added:' + fake_task)
print('work queue length: ' + str(ret))
