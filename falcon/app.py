# app.py

import os
import sys
import falcon
import json
import redis
import logging
#from falcon_cors import CORS
import falcon_cors

# Let's get this party started
# http://redis.io/commands/rpoplpush

opts = { 'host': os.environ.get('REDIS_HOST'), 'port': 6379 }

password = os.environ.get('REDIS_PASSWORD')
if password is not None:
    opts['password'] = password

r = redis.StrictRedis(**opts)

work_queue = 'work'

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.

class MainHandler:
    """docstring for MainHandler"""
    def on_get(self, req, resp):
        try:
            data = "Hello Welcome to Docker -> Nginx -> Gunicorn -> Falcon\n"
            resp.body = data
        except Exception as e:
            print(e)
            resp.body = "error"
 
class TaskResource:
#    def __init__(self):
#        self.logger = logging.getLogger('falconapp.' + __name__)

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        ret = r.llen(work_queue)

        resp.body = json.dumps({'queue_name': work_queue, 'queue_size': ret})

    def on_post(self, req, resp):
        """Handles POST requests"""

        resp.status = falcon.HTTP_200  # This is the default status
        fake_task = req.get_param('task', required=True)
        ret = r.lpush(work_queue, fake_task)
        # Todo: exception handling
        resp.body = ('task added:' + fake_task + 
            'work queue length: ' + str(ret))

cors = falcon_cors.CORS(allow_origins_list=['pyzam.com', 'pyz.am', 'http://pyz.am'])
falcon_cors.log.get_default_logger().setLevel(logging.DEBUG)

# falcon.API instances are callable WSGI apps
app = falcon.API(middleware=[cors.middleware])

# Set any urlencoded form posts to be able to be gotten by get_param
falcon.RequestOptions.auto_parse_form_urlencoded = True
# json.loads(raw_json, encoding='utf-8')

# Resources are represented by long-lived class instances
tasks = TaskResource()

# tasks will handle all requests to the '/tasks' URL path
app.add_route('/tasks', tasks)
app.add_route('/', MainHandler())
