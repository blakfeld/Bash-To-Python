"""
tail.py -- Emulate UNIX tail.

Author: Corwin Brown
E-Mail: blakfeld@gmail.com
Date: 5/24/2015
"""

import sys
import time


class Tail(object):

    BLOCK_SIZE = 512
    SLEEP_INTERVAL = 1.0

    def __init__(self, stdin=None, fname=None, num_lines=10, watch=False):
        """
        Constructor

        Args:
            args (list): Any command line arguments.
        """

        self.stdin = stdin
        self.fname = fname
        self.num_lines = num_lines
        self.watch = watch

    def run(self):
        """
        Emulate UNIX tail
        """

        if self.stdin:
            self._tail_stdin(self.stdin, self.num_lines)
            return

        if isinstance(self.fname, list):
            if len(self.fname) > 1:
                for f in self.fname:
                    self._validate_file(f)
                    print('\n==> {} <=='.format(f))
                    self._tail_lines(f, self.num_lines)
                return

            else:
                self._validate_file(self.fname[0])
                if self.watch:
                    self._tail_watch(self.fname[0], self.num_lines)
                else:
                    self._tail_lines(self.fname[0], self.num_lines)

                return

        else:
            self._validate_file(self.fname)
            if self.watch:
                self._tail_watch(self.fname, self.num_lines)
            else:
                self._tail_lines(self.fname, self.num_lines)
            return

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
                    f.seek(0, 0)
                    blocks.append(f.read(file_end_byte))

                # Count the number of newlines to see how many lines we have
                #   left to find.
                lines_to_go -= blocks[-1].count('\n')
                block_number -= 1

            # Reverse the output so we get top to bottom.
            tail_text = ''.join(reversed(blocks))

            # Truncate off any extra lines and return.
            sys.stdout.write('\n'.join(tail_text.splitlines()[-num_lines:]))

    def _tail_stdin(self, stdin, num_lines=10):
        """
        Print the last n lines of stdin.

        Args:
            stdin (str): Essentially the output of 'sys.stdin.read()'
        """

        sys.stdout.write('\n'.join(stdin.split('\n')[-num_lines:]))

    def _tail_watch(self, fname, num_lines=10):
        """
        Continuously watch a file and print all new lines.

        We already have a function to print the last n lines, lets just call
            that, then reopen that file and watch it. It could be more
            efficient, but file handles are pretty cheap.

        Args:
            fname (str): The file to watch.
        """

        self._tail_lines(fname, num_lines)

        with open(fname, 'r') as f:
            f.seek(0, 2)

            while True:
                # Find the end of the file, see if it contains any data,
                #   if not, sleep, then seek back to that same point, and
                #   check again.
                file_end_byte = f.tell()
                line = f.readline()
                if not line:
                    time.sleep(self.SLEEP_INTERVAL)
                    f.seek(file_end_byte)
                else:
                    sys.stdout.write(line)

    def _validate_file(self, fname):
        """
        Ensure that the provided file exists.

        Args:
            fname (str): The file to validate.

        Raises:
            ValueError: If fname does not exist.
        """

        if not os.path.exists(fname):
            raise ValueError('tail: {}: No such file or directory.'
                             .format(fname))
        pass
