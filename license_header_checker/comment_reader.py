# Copyright (c) 2023 Vadym Zakovinko
# SPDX-License-Identifier: MIT

from license_header_checker.exceptions import CommentStyleBadFormatException


class CommentReader:

    def __init__(self, comment_style):
        self.multiline = False
        self.prefix = comment_style

        if '|' in comment_style:
            parts = comment_style.split('|')
            if len(parts) != 3:
                raise CommentStyleBadFormatException()

            self.multiline = True
            self.start, self.prefix, self.end = parts

    def read(self, file_handle):
        func = self._read_singleline_comments
        if self.multiline:
            func = self._read_multiline_comments

        return func(file_handle)

    def _read_singleline_comments(self, file_handle):
        content = []
        for line in file_handle:
            if line.startswith(self.prefix):
                content.append(line[len(self.prefix):].strip(' '))
            else:
                break

        return ''.join(content)

    def _read_multiline_comments(self, file_handle):
        content = []
        for i, line in enumerate(file_handle):
            if len(content) == 0:
                if line.startswith(self.start):
                    content.append(line[len(self.start):])
            else:
                if line.rstrip().endswith(self.end):
                    content.append(line[:line.index(self.end)])
                    break
                elif line.startswith(self.prefix):
                    content.append(line[len(self.prefix):])
                else:
                    break

        return ''.join(map(lambda s: s.strip(' '), content))
