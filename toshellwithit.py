from collections import namedtuple
from collections import OrderedDict
from inspect import getargspec
from inspect import getdoc
from inspect import ismethod
from itertools import chain
import json
import sys

Command = namedtuple('Command', 'method, req_args_list, opt_args_dict')


class ToShellWithIt(object):

    def __init__(self, tool_class, help=True):
        self.tool_class = tool_class
        self.commands = self._get_commands_dict(tool_class)

        if help:
            self.commands["help"] = Command(
                self.print_help, [], {"command": None})

    def _get_commands_dict(self, tool_class):
        commands = {}

        for method_name in tool_class.__dict__.keys():
            method = getattr(tool_class, method_name)

            if ismethod(method) and not method_name.startswith("_"):
                req_args, opt_args = self._get_command_args(
                    tool_class, method_name)
                commands[method_name] = Command(method, req_args, opt_args)

        return commands

    def _get_command_args(self, tool_class, command):
        argspec = getargspec(getattr(tool_class, command))

        if argspec.defaults:
            num_kw_args = len(argspec.defaults) if argspec.defaults else -1
            req_args = argspec.args[1:-num_kw_args]
            opt_args = OrderedDict(
                zip(argspec.args[-num_kw_args:], argspec.defaults))
        else:
            req_args = argspec.args[1:]
            opt_args = OrderedDict()

        return req_args, opt_args

    def usage(self):
        print("Usage: {0} command [args...]".format(sys.argv[0]))
        print("")
        print("Available commands and parameters:")

        for command, command_info in sorted(self.commands.items()):
            if command == "help":
                print("   {0:40s} {1}".format("help", "[command]"))
            else:
                req_args = command_info.req_args_list
                opt_args = command_info.opt_args_dict

                req_args_str = " " + " ".join(req_args) if req_args else ""
                opt_args_str = " " + \
                    " ".join(
                        ["[" + opt_arg + "]" for opt_arg in opt_args.keys()])

                print("   {0:40s}{1}{2}".format(
                    command, req_args_str, opt_args_str))

        print("")

    def print_help(self, command=None):
        """
        Prints the docstring associated with the given command.
        """
        if not command:
            self.usage()
        elif command in self.commands:
            print getdoc(self.commands[command].method)
        else:
            raise Exception("{0} is not a valid command\n".format(command))

    def parse_arguments(self, raw_args):
        args = [arg for arg in raw_args if "=" not in arg]
        kwargs = dict(tuple(arg.split("=")) for arg in raw_args if "=" in arg)

        return args, kwargs

    def run_command(self, cmd, args, kwargs):
        req_args = self.commands[cmd].req_args_list
        opt_args = self.commands[cmd].opt_args_dict

        if len(args) < len(req_args) or len(req_args) + len(opt_args) < len(args):
            raise Exception("Incorrect # of arguments for {0}\n".format(cmd))

        return self.commands[cmd].method(*args, **kwargs)

    def run(self):
        # check for command
        if len(sys.argv) <= 1:
            self.usage()
            sys.exit(0)

        # get arguments
        command, arguments = sys.argv[1], sys.argv[2:]
        args, kwargs = self.parse_arguments(arguments)

        # check if command exists
        if command not in self.commands:
            sys.stderr.write("{0} is not a valid command\n".format(command))
            self.usage()
            sys.exit(1)

        # run the command
        try:
            return_value = self.run_command(command, args, kwargs)
            if return_value:
                print(json.dumps(return_value))
        except Exception, e:
            sys.stderr.write(str(e))
            sys.exit(1)
