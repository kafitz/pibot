#!/usr/bin/env python
"""
__init__.py - Phenny Init Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import sys, os, time, threading, signal
import bot

class Watcher(object): 
   # Cf. http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496735
   def __init__(self, config_file):
      config_dir = os.path.dirname(config_file)
      config_name = os.path.basename(config_file).split('.')[0]

      self.child = os.fork()
      if self.child != 0: 
         pid_file = '{}/phenny.{}.pid'.format(config_dir, config_name)
         with open(pid_file, 'w') as f:
            f.write(str(self.child))
         self.watch()

   def watch(self):
      try: os.wait()
      except KeyboardInterrupt:
         self.kill()
      sys.exit()

   def kill(self):
      try: os.kill(self.child, signal.SIGKILL)
      except OSError: pass

def run_phenny(config): 
   if hasattr(config, 'delay'): 
      delay = config.delay
   else: delay = 20

   def connect(config): 
      p = bot.Phenny(config)
      try:
         port = int(config.port)
      except ValueError:
         print >> sys.stderr, 'Error: Port set to', config.port
         sys.exit()
      p.run(config.host, port)

   try: Watcher(config.filename)
   except Exception, e: 
      print >> sys.stderr, 'Warning:', e, '(in __init__.py)'

   while True: 
      try: connect(config)
      except KeyboardInterrupt: 
         sys.exit()

      if not isinstance(delay, int): 
         break

      warning = 'Warning: Disconnected. Reconnecting in %s seconds...' % delay
      print >> sys.stderr, warning
      time.sleep(delay)

def run(config): 
   t = threading.Thread(target=run_phenny, args=(config,))
   if hasattr(t, 'run'): 
      t.run()
   else: t.start()

if __name__ == '__main__': 
   print __doc__
