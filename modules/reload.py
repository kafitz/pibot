#!/usr/bin/env python
"""
reload.py - Phenny Module Reloader Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import sys, os.path, time, imp
import irc

def f_load(phenny, input):
   if not input.admin: return phenny.say("Need to be admin to execute.")

   name = input.group(2)
   if name == phenny.config.owner: 
      return phenny.reply('What?')

   if (not name) or (name == '*'): 
      phenny.variables = None
      phenny.commands = None
      phenny.setup()
      return phenny.reply('done')

   path = os.path.dirname(sys.modules['admin'].__file__)
   module = imp.load_source(name, path)
   sys.modules[name] = module
   if hasattr(module, 'setup'): 
      module.setup(phenny)

   mtime = os.path.getmtime(module.__file__)
   modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

   phenny.register(vars(module))
   phenny.bind_commands()

   phenny.reply('%r (version: %s)' % (module, modified))
f_load.name = 'load'
f_load.rule = ('$nick', ['load'], r'(\S+)?')
f_load.priority = 'low'
f_load.thread = False

def f_reload(phenny, input): 
   """Reloads a module, for use by admins only.""" 
   if not input.admin: return phenny.say("Need to be admin to execute.")

   name = input.group(2)
   if name == phenny.config.owner: 
      return phenny.reply('What?')

   if (not name) or (name == '*'): 
      phenny.variables = None
      phenny.commands = None
      phenny.setup()
      return phenny.reply('done')

   if not sys.modules.has_key(name): 
      return phenny.reply('%s: no such module!' % name)

   # Thanks to moot for prodding me on this
   path = sys.modules[name].__file__
   if path.endswith('.pyc') or path.endswith('.pyo'): 
      path = path[:-1]
   if not os.path.isfile(path): 
      return phenny.reply('Found %s, but not the source file' % name)

   module = imp.load_source(name, path)
   sys.modules[name] = module
   if hasattr(module, 'setup'): 
      module.setup(phenny)

   mtime = os.path.getmtime(module.__file__)
   modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

   phenny.register(vars(module))
   phenny.bind_commands()

   phenny.reply('%r (version: %s)' % (module, modified))
f_reload.name = 'reload'
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'low'
f_reload.thread = False

if __name__ == '__main__': 
   print __doc__.strip()
