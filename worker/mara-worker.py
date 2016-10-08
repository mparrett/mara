import redis
import signal
import sys
import subprocess
import os
import logging

from tasks.pillow_example import test_gen


logging.basicConfig(filename='/var/log/mara-worker.log', level=logging.DEBUG)

def signal_handler(signal, frame):
    logging.info('You pressed Ctrl+C!')
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

processing_queue = 'processing-' + str(worker_id)
work_queue = 'work'

start_msg = "Worker ID " + str(worker_id) + " started"
logging.info(start_msg)
print(start_msg)

while True:
    logging.info("Waiting on work queue")

    task = r.brpoplpush(work_queue, processing_queue, 0)
    if task is None: 
        logging.warning("Empty task. This should not happen")
        continue

    logging.info(task)
    logging.info("Grabbed a task from the work queue into my processing queue")
   
    # Grabbed a task into the processing queue. There could be some latency
    # But usually not

    # ...

    # Work on the task
    tasks = r.lrange(processing_queue, 0, 0) # Could just use "task" from above, pop when finished successfully
    task = tasks.pop().decode('ascii') # Is this decode correct?
    task_parts = task.split(' ')
    
    cmd = task_parts[0]
    args = task_parts[1:]

    if cmd == 'test_gen':
        logging.info('Running test_gen with args ' + ','.join(args))
        test_gen(*args)
        continue

    if cmd == 'test_sub':
        logging.info('Running ' + task)
        try:
            output = subprocess.check_output(args)
            
            logging.info('Output ' + str(output))

            removed = r.lrem(processing_queue, -1, task)

        except subprocess.CalledProcessError as e:
            logging.warning('Command failed:')
            logging.warning(str(e.returncode))
            logging.warning(e.cmd)
            logging.warning(e.output)
            # Todo: push to failed queue
        continue
    logging.info('Unknown command: ' + cmd)

