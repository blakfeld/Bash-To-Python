"""
tail.py -- Emulate UNIX tail.

Author: Corwin Brown
E-Mail: blakfeld@gmail.com
Date: 5/24/2015
"""

from argparse import ArgumentParser


class Tail(object):

    BLOCK_SIZE = 512

    def __init__(self, args):
        """
        Constructor

        Args:
            args (list): Any command line arguments.
        """

        self.args = self.parser(args)

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

        parser = ArgumentParser(description='tail -- '
                                            'display the last part of a file')

        parser.add_argument('infile',
                            type=str,
                            metavar='file',
                            help='The file to tail')
        parser.add_argument('-n',
                            type=int,
                            metavar='number',
                            help='The location is number lines.')

        return parser.parse_args()

    def _tail_lines(self, fname, num_lines=10):
        """
        Print the last n lines of a file.

        Here we will navigate to the end of a file, then march backwards
            at some interval (defined by self.BLOCK_SIZE), then count the
            number of newlines we have. Once we have greater than or equal
            newlines, truncate off any extra, and return.

        Args:
            fname (str): The file to tail.
            num_lines (int): The number of lines from the bottom to display.
        """

        block_number = -1
        lines_to_go = num_lines
        blocks = []
        with open(fname, 'r') as f:
            f.seek(0, 2)

            # Mark the ending byte, so we don't try to read past it.
            file_end_byte = f.tell()

            while lines_to_go > 0 and file_end_byte > 0:
                # If we aren't at the end, backup and read a new block.
                if file_end_byte - self.BLOCK_SIZE > 0:
                    f.seek(self.BLOCK_SIZE * block_number, 2)
                    blocks.append(f.read(self.BLOCK_SIZE))

                else:
                    blocks.append(f.read(self.BLOCK_SIZE))

                # Count the number of newlines to see how many lines we have
                #   left to find.
                lines_to_go -= blocks[-1].count('\n')
                block_number -= 1

            # Reverse the output so we get top to bottom.
            tail_text = ''.join(reversed(blocks))

            # Truncate off any extra lines and return.
            return '\n'.join(tail_text.splitlines()[-num_lines:])

    def _tail_stdin(stdin, num_lines=10):
        """
        Print the last n lines of stdin.

        Args:
            stdin (str): Essentially the output of 'sys.stdin.read()'
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
        Ensure that the provided file exists.

        Args:
            fname (str): The file to validate.

        Raises:
            ValueError: If fname does not exist.
        """

        pass
