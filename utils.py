#!/usr/bin/env python

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

   @classmethod
   def method_with_keyword_args(cls, kw_arg1="default1", kw_arg2="default2"):
      """
      This method has keyword args (kw_arg1, kw_arg2).
      """
      print("method_with_keyword_args")

   @classmethod
   def method_with_positional_and_keyword_args(cls, pos_arg1, pos_arg2, kw_arg1="default1", kw_arg2="default2"):
      """
      This method has positional args (pos_arg1, pos_arg2) and keyword args (kw_arg1, kw_arg2).
      """
      print("method_with_positional_and_keyword_args")

if __name__ == '__main__':
   from toshellwithit import ToShellWithIt
   ToShellWithIt(Utils).run()
