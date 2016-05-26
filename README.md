## ToShellWithIt
ToShellWithIt makes it simple to call Python methods from the command line. 

With ToShellWithIt, a Python method can be called from the shell or a shell script using familiar syntax, e.g. `utils.py args1 args2`. Return codes follow shell conventions. i.e. 0 for success, 1 for error.

#### Contract
1. Per Python convention, methods that start with '_' are considered private.
2. Only @classmethods are runnable.
3. Successful execution returns exit code 0. An exception results in exit code 1 being returned.
4. If the method returns an object, the object's JSON representation is printed.
5. A `help` command is provided. `./utils.py help [command]` prints the relevant docstring.

#### Usage
At the bottom of your script, add:
```python
if __name__ == '__main__':
   from toshellwithit import ToShellWithIt
   ToShellWithIt(Utils).run()
```

#### Example
```python
class Utils:

    @classmethod
    def method_with_no_args(cls):
        """
        This method method_with_no_args has no args.
        """
        print("method_with_no_args")

    @classmethod
    def method_with_positional_args(cls, pos_arg1, pos_arg2):
        """
        This method has positional args (pos_arg1, pos_arg2).
        """
        print("method_with_positional_args")
        print("   pos_arg1: {0}, pos_arg2: {1}".format(pos_arg1, pos_arg2))

    @classmethod
    def method_with_keyword_args(cls, kw_arg1="default1", kw_arg2="default2"):
        """
        This method has keyword args (kw_arg1, kw_arg2).
        """
        print("method_with_keyword_args")
        print("   kw_arg1: {0}, kw_arg2: {1}".format(kw_arg1, kw_arg2))

if __name__ == '__main__':
    from toshellwithit import ToShellWithIt
    ToShellWithIt(Utils).run()
```

#### Output
```
$> ./utils.py
Usage: ./utils.py command [args...]

Available commands and the parameters:
   help                                     [command]
   tool_method_keyword_args                 [kw_arg1] [kw_arg2]
   tool_method_no_args                      
   tool_method_positional_and_keyword_args  pos_arg1 pos_arg2 [kw_arg1] [kw_arg2]
   tool_method_positional_args              pos_arg1 pos_arg2 

$> ./utils.py help tool_method_keyword_args
This method has keyword args (kw_arg1, kw_arg2).

$> ./utils.py method_with_positional_args 1 2
method_with_positional_args
   pos_arg1: 1, pos_arg2: 2

$> ./utils.py method_with_positional_and_keyword_args 1 kw_arg2=2 2
method_with_positional_and_keyword_args
   pos_arg1: 1, pos_arg2: 2
   kw_arg1: default1, kw_arg2: 2

$> echo $?
0

$> ./utils.py method_with_no_args 2
Incorrect # of arguments for method_with_no_args

$> echo $?
1
```
