from unittest import mock

import pytest
import termcolor

from license_header_checker.checker import LicenseHeaderChecker
from license_header_checker.reporter import TermReporter


def test_default_reporter():
    checker = LicenseHeaderChecker()
    assert isinstance(checker.reporter, TermReporter)


def test_custom_reporter():

    class R:
        pass

    checker = LicenseHeaderChecker(reporter_cls=R)
    assert isinstance(checker.reporter, R)


@pytest.mark.parametrize(
    ('filename', 'content', 'result'),
    (
        ('some/path/to/source.c', '# 123\ncode', 0),
        ('some/path/to/source.c', '# Hello\ncode', 1),
    )
)
def test_checker_run(filename, content, result):
    checker = LicenseHeaderChecker()

    args = mock.Mock(
        filenames=(filename, ),
        license=r'\d+',
        comment_style='#'
    )

    with mock.patch('builtins.open', mock.mock_open(read_data=content)) as m_open:
        assert checker.run(args) == result

    m_open.assert_called_with(filename, 'r')


def test_fail_resolution__bad_format():
    content = '\nCopyright (c) 2020 Geanix ApS, Pete Johanson\n\nSPDX-License-Identifier: Apache-2.0\n'
    regex = r'\nCopyright \(c\) \d{4} The ZMK Contributors\n\nSPDX-License-Identifier: MIT\n'

    checker = LicenseHeaderChecker()
    resolution = checker._get_fail_resolution(regex, content)

    assert resolution.resolution == 'license has bad format'
    assert resolution.details == (
        termcolor.colored(content[:20], 'green')
        + termcolor.colored(content[20:], 'red')
    )


def test_fail_resolution__missing_header():
    checker = LicenseHeaderChecker()
    resolution = checker._get_fail_resolution(r'.*', '')

    assert resolution.resolution == checker.reporter.resolution_no_header().resolution


@pytest.mark.parametrize(
    ('cmdline', 'expected_args'),
    (
        (
            ['--license', '\\d{3}'],
            {'comment_style': '#', 'license': r'\d{3}', 'filenames': []},
        ),
        (
            ['--license', '\\d{3}', '--comment-style', '@'],
            {'comment_style': '@', 'license': r'\d{3}', 'filenames': []},
        ),
        (
            ['--license', '\\d{3}', '--comment-style', '/*| *| */'],
            {'comment_style': '/*| *| */', 'license': r'\d{3}', 'filenames': []},
        ),
        (
            ['--license', '\\w{3}', 'one.c', 'two.c', 'one.h'],
            {'comment_style': '#', 'license': r'\w{3}', 'filenames': ['one.c', 'two.c', 'one.h']},
        ),
    )
)
def test_args_parser(cmdline, expected_args):
    parser = LicenseHeaderChecker.get_args_parser()
    args = parser.parse_args(cmdline)

    assert args.__dict__ == expected_args


def test_comment_style_bad_format():
    with mock.patch('sys.exit') as m_exit:
        with mock.patch('builtins.print') as m_print:
            LicenseHeaderChecker().run(
                mock.Mock(
                    comment_style='|',
                    license=r'.*',
                    filenames=[]
                )
            )

    m_exit.assert_called_with(1)
    m_print.assert_called_with('Impropper configuration: bad comment style format')
