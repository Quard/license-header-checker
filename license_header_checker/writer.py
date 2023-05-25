# Copyright (c) 2023 Vadym Zakovinko
# SPDX-License-Identifier: MIT

from datetime import date
from functools import lru_cache

from license_header_checker.exceptions import CommentStyleBadFormatException


class LicenseWriter:

    def __init__(self, comment_style, tmpl_fh):
        self.multiline = False
        self.prefix = comment_style

        if '|' in comment_style:
            parts = comment_style.split('|')
            if len(parts) != 3:
                raise CommentStyleBadFormatException()

            self.multiline = True
            self.start, self.prefix, self.end = parts

        self.tmpl_fh = tmpl_fh

    def write(self, file_handle):
        file_handle.seek(0)
        content = file_handle.read()
        file_handle.seek(0)
        tmpl = self._get_template()
        line_end = self._get_line_end(tmpl)

        if self.multiline:
            file_handle.write(f'{self.start}{line_end}')

        for line in tmpl.split(line_end):
            file_handle.write(f'{self.prefix} {line}'.rstrip(' '))
            file_handle.write(line_end)

        if self.multiline:
            file_handle.write(f'{self.end}{line_end}{line_end}')
        else:
            file_handle.write(line_end)

        file_handle.write(content)

    @lru_cache()
    def _get_template(self):
        template = self.tmpl_fh.read()

        template = template.replace('{YEAR}', str(date.today().year))

        return template

    @lru_cache()
    def _get_line_end(self, tmpl):
        for lineend in ('\r\n', '\n'):
            if lineend in tmpl:
                return lineend

        return '\n'
