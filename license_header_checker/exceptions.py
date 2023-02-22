# Copyright (c) 2023 Vadym Zakovinko
# SPDX-License-Identifier: MIT


class LicenseHeaderCheckerException(Exception):
    pass


class CommentStyleBadFormatException(LicenseHeaderCheckerException):
    message = 'Bad format of comment style'
