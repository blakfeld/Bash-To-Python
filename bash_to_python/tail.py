"""
tail.py -- Emulate UNIX tail.

Author: Corwin Brown
E-Mail: blakfeld@gmail.com
Date: 5/24/2015
"""

from argparse import ArgumentParser


class Tail(object):

    def __init__(self, args):
        """
        Constructor

        Args:
            args (list): Any command line arguments.
        """

        self.args = args

    def run(self):
        """
        Emulate UNIX tail
        """

        pass

    def _parser(self, args):
        """
        Parse command line args.

        Args:
            args (list): Args from the command line.
        """

        parser = ArgumentParser(description='The tail utility displays the '
                                            'contents of file or, by default, '
                                            'its standard input, to the '
                                            'standard output.')

        return parser.parse_args()

    def _tail_lines(fname, num_lines=10):
        """
        Print the last n lines of a file.

        Args:
            fname (str): The file to tail.
            num_lines (int): The number of lines from the bottom to display.
        """

        pass

    def _tail_watch(self, fname):
        """
        Continuously watch a file and print all new lines.

        Args:
            fname (str): The file to watch.
        """

        pass

    def _validate_file(self, fname):
        """
        Ensure that the provided file exists and is not a directory.

        Args:
            fname (str): The file to validate.

        Raises:
            ValueError: If fname does not exist or is a directory.
        """

        pass
