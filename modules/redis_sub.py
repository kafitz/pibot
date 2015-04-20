from datetime import datetime
import json
import redis
import threading
import time

def callback(phenny):
    r = redis.client.StrictRedis()
    sub = r.pubsub()
    sub.subscribe('irc_msg')
    while True:
        for m in sub.listen():
            if m['type'] == 'message':
                data = json.loads(m['data'])
                channel = data['channel']
                message = data['text']
                phenny.msg(channel, message)  #'Recieved: {0}'.format(m['data'])

def start(phenny):
    t = threading.Thread(target=callback, args=(phenny,))
    t.setDaemon(True)
    t.start()
    while True:
        now = datetime.now().replace(microsecond=0)
        print '{} -- redis listener: waiting'.format(now)
        time.sleep(300)

if __name__ == '__main__':
    main()