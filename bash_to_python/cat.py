"""
cat.py -- Emulate UNIX cat.

Author: Corwin Brown
E-Mail: blakfeld@gmail.com
Date: 5/25/2015
"""

import os
import sys


class Cat(object):

    def __init__(self, fname=None, stdin=None):
        """
        Constructor

        Args:
            fname (str): File to print to screen
            stdin (str): Input from sys.stdin to output.

        Raises:
            ValueError: If provided file doesn't exist or is a directory.
        """

        self.fname = fname
        self.stdin = stdin

    def run(self):
        """
        Emulate 'cat'.

        Echo User input if a file is not provided, if a file is provided, print
            it to the screen.
        """

        if self.stdin:
            self._cat_stdin(self.stdin)
            return

        if not self.fname:
            self._cat_input()
            return

        if isinstance(self.fname, list):
            for f in self.fname:
                self._validate_file(f)
                self._cat_file(f)
        else:
            self._validate_file(self.fname)
            self._cat_file(self.fname)

    def _cat_stdin(self, stdin):
        """
        Print data provided in stdin.

        Args:
            stdin (str): The output of sys.stdin.read()
        """

        print stdin

    def _cat_file(self, fname):
        """
        Print contents of a file.

        Args:
            fname: Name of file to print.
        """

        with open(fname, 'r') as f:
            sys.stdout.write((f.read()))

    def _cat_input(self):
        """
        Echo back user input.
        """

        while True:
            user_input = raw_input()
            sys.stdout.write(user_input)

    def _validate_file(self, fname):
        """
        Ensure fname exists, and is not a directory.

        Args:
            fname (str): The file path to validate.

        Raises:
            ValueError: If file does not exist or is a directory.
        """

        if not os.path.exists(fname):
            raise ValueError('cat: {}: No such file or directory.'
                             .format(fname))
        if os.path.isdir(fname):
            raise ValueError('cat: {}: Is a directory.'
                             .format(fname))
