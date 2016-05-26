from inspect import getargspec
from inspect import getdoc
from inspect import ismethod
import json
import sys

class ToShellWithIt(object):
   def __init__(self, tool_class, help=True):
      self.tool_class   = tool_class
      self.commands     = ["help"] if help else []

      if tool_class.__dict__:
         for method in tool_class.__dict__.keys():
            if ismethod(getattr(tool_class, method)) and not method.startswith("_"):
               self.commands.append(method)
         self.commands.sort()

   def _get_signature(self, command):
      if command == "help":
         return [], ["command"]

      argspec = getargspec(getattr(self.tool_class, command))

      if argspec.defaults:
         num_kw_args = len(argspec.defaults) if argspec.defaults else -1
         req_args = argspec.args[1:-num_kw_args]
         opt_args = argspec.args[-num_kw_args:]
      else:
         req_args = argspec.args[1:]
         opt_args = []

      return req_args, opt_args

   def usage(self):
      print("Usage: {0} command [args...]".format(sys.argv[0]))
      print("")
      print("Available commands and parameters:")

      for command in self.commands:
         if False and command == "help":
            print("   {0:40s} {1}".format("help", "[command]"))
         else:
            req_args, opt_args = self._get_signature(command)

            req_args_str = " " + " ".join(req_args) if req_args else ""
            opt_args_str = " " + " ".join(["[" + opt_arg + "]" for opt_arg in opt_args])

            print("   {0:40s}{1}{2}".format(command, req_args_str, opt_args_str))

      print("")

   def print_help(self, command=None):
      # check correct help usage
      if command is list and len(command) > 1:
         raise Exception("Incorrect # of arguments for help\n".format(command))

      # print usage
      if not command:
         self.usage()
      elif command in self.tool_class.__dict__:
         print(getdoc(getattr(self.tool_class, command)))
      else:
         raise Exception("{0} is not a valid command\n".format(command))

   def is_valid_command(self, command):
      return command == "help" or command in self.tool_class.__dict__

   def run_command(self, cmd, args, kwargs):
      # get argspec
      argspec = getargspec(getattr(self.tool_class, cmd))

      if argspec.defaults:
         req_args = argspec.args[1:-len(argspec.defaults)]
         opt_args = argspec.args[-len(argspec.defaults):]
      else:
         req_args = argspec.args[1:]
         opt_args = []

      # check if correct # of arguments
      if len(args) < len(req_args) or len(args) > len(req_args) + len(opt_args):
         raise Exception("Incorrect # of arguments for {0}\n".format(cmd))

      return getattr(self.tool_class, cmd)(*args, **kwargs)

   def parse_args(self, arglist):
      if len(arglist) <= 1:
         self.usage()
         sys.exit(0)

      command, arguments = arglist[1], arglist[2:]
      return command, arguments

   def run(self):
      # get arguments
      command, arguments = self.parse_args(sys.argv)
   
      # check if command exists
      if not self.is_valid_command(command):
         sys.stderr.write("{0} is not a valid command\n".format(command))
         self.usage()
         sys.exit(1)

      # run the command
      try:
         if command == "help":
            self.print_help(arguments[0] if arguments else None)
         else:
            return_value = self.run_command(command, arguments, {})
            if return_value:
               print(json.dumps(return_value))
      except Exception, e:
         sys.stderr.write(str(e))
         sys.exit(1)
