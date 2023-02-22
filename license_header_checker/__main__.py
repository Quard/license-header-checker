# Copyright (c) 2023 Vadym Zakovinko
# SPDX-License-Identifier: MIT

import sys

from license_header_checker.checker import LicenseHeaderChecker


def main():
    parser = LicenseHeaderChecker.get_args_parser()

    checker = LicenseHeaderChecker()
    ret_code = checker.run(parser.parse_args())
    if ret_code:
        checker.reporter.report()

    sys.exit(ret_code)


if __name__ == '__main__':
    main()
