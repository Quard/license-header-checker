# Copyright (c) 2023 Vadym Zakovinko
# SPDX-License-Identifier: MIT

import argparse
import re
import sys

from license_header_checker.comment_reader import CommentReader
from license_header_checker.exceptions import CommentStyleBadFormatException
from license_header_checker.reporter import TermReporter


class LicenseHeaderChecker:

    def __init__(self, reporter_cls=None):
        if reporter_cls is None:
            reporter_cls = TermReporter

        self.reporter = reporter_cls()

    def run(self, args):
        try:
            reader = CommentReader(args.comment_style)
        except CommentStyleBadFormatException:
            print('Impropper configuration: bad comment style format')
            sys.exit(1)

        license = re.compile(args.license)
        for filename in args.filenames:
            with open(filename, 'r') as fh:
                header = reader.read(fh)
                if not license.match(header):
                    self.reporter.add(filename, self._get_fail_resolution(args.license, header))

        return len(self.reporter)

    def _get_fail_resolution(self, regex, content):
        if not content:
            return self.reporter.resolution_no_header()

        last_good = 0
        for i in range(2, len(regex)):
            _regex = regex[:i]
            try:
                match = re.match(_regex, content)
                if match:
                    last_good = match.end()
            except re.error:
                pass

        return self.reporter.resolution_bad_license(content, last_good)

    @staticmethod
    def get_args_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument('filenames', nargs='*', help='list of files to check')
        parser.add_argument(
            '--comment-style',
            default='#',
            help=(
                'comment prefix, also supports multiline comments with [<start>|<prefix>|<end>]'
                ' syntax, like "/*| *| */" for C'
            )
        )
        parser.add_argument('--license', help='required license regex')

        return parser
