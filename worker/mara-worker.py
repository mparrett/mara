import redis
import signal
import sys
import subprocess
import os

from tasks.pillow_example import test_gen

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# http://redis.io/commands/rpoplpush

opts = { 'host': os.environ.get('REDIS_HOST'), 'port': 6379 }

password = os.environ.get('REDIS_PASSWORD')
if password is not None:
    opts['password'] = password

r = redis.StrictRedis(**opts)

worker_id = 1
if len(sys.argv) >= 2:
    worker_id = sys.argv[1]

processing_queue = str(worker_id) + '-queue'
work_queue = 'work'

print("Worker ID " + str(worker_id) + " started")

while True:
    print("Waiting on work queue")

    task = r.brpoplpush(work_queue, processing_queue, 0)
    if task is None: 
        print("Empty task. This should not happen")
        continue

    print(task) # todo: check return?
    print("Grabbed a task from the work queue into my processing queue")
   
    # Work on the task
    tasks = r.lrange(processing_queue, 0, 0)
    task = tasks.pop().decode('ascii') # Is this decode correct?
    task_parts = task.split(' ')
    
    cmd = task_parts[0]
    args = task_parts[1:]

    if cmd == 'test_gen':
        print('Running test_gen with args ' + args[0])
        test_gen(args[0])

    if cmd == 'test_sub':
        print('Running ' + task)
        try:
            output = subprocess.check_output(args)
            
            print('Output ' + str(output))

            removed = r.lrem(processing_queue, -1, task)

        except subprocess.CalledProcessError as e:
            print('Command failed:')
            print(str(e.returncode))
            print(e.cmd)
            print(e.output)
            # Todo: push to failed queue

