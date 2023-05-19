from io import StringIO

import pytest

from license_header_checker.exceptions import CommentStyleBadFormatException
from license_header_checker.reader import CommentReader


@pytest.mark.parametrize(
    ('content', 'expected_result'),
    (
        (
            '# Single line',
            'Single line'
        ),
        (
            '# First line\n#\n# Second line',
            'First line\n\nSecond line'
        ),
    )
)
def test_single_comment(content, expected_result):
    io = StringIO(content)

    reader = CommentReader('#')

    assert reader.read(io) == expected_result


@pytest.mark.parametrize(
    ('content', 'expected_result'),
    (
        (
            '/*\n * Single line\n */',
            '\nSingle line\n'
        ),
        (
            (
                '/*\n'
                ' * First line\n'
                ' * Second line\n'
                ' */'
            ),
            '\nFirst line\nSecond line\n'
        ),
        (
            (
                '/*\n'
                ' * First line\n'
                ' *\n'
                ' * Second line\n'
                ' */'
            ),
            '\nFirst line\n\nSecond line\n'
        ),
    )
)
def test_multiline_comment(content, expected_result):
    io = StringIO(content)

    reader = CommentReader('/*| *| */')

    assert reader.read(io) == expected_result


def test_malformed_multiline_comment():
    io = StringIO(
        '/*\n'
        ' * First line\n'
        ' * Second line\n'
        'comment not closed'
    )

    reader = CommentReader('/*| *| */')

    assert reader.read(io) == '\nFirst line\nSecond line\n'


@pytest.mark.parametrize(
    ('comment_style', 'content', 'expected_result'),
    (
        ('#', '# comment line\ncode line\n', 'comment line\n'),
        ('#', '# comment line\n# second comment line\ncode line\n', 'comment line\nsecond comment line\n'),
        ('//', '// comment line\ncode line\n', 'comment line\n'),
        ('//', '// comment line\n// second comment line\ncode line\n', 'comment line\nsecond comment line\n'),
        ('REM', 'REM comment line\ncode line\n', 'comment line\n'),
        ('REM', 'REM comment line\nREM second comment line\ncode line\n', 'comment line\nsecond comment line\n'),
        (
            '/*| *| */',
            (
                '/*\n'
                ' * comment line\n'
                ' */\n'
                'code line\n'
            ),
            '\ncomment line\n'
        ),
        (
            '/*| *| */',
            (
                '/*\n'
                ' * comment line\n'
                ' * second comment line\n'
                ' */\n'
                'code line\n'
            ),
            '\ncomment line\nsecond comment line\n'
        ),
    )
)
def test_comment_styles(comment_style, content, expected_result):
    io = StringIO(content)

    reader = CommentReader(comment_style)

    assert reader.read(io) == expected_result


@pytest.mark.parametrize(
    ('comment_style', ),
    (
        ('|', ),
        ('|||', ),
    )
)
def test_comment_style_bad_format(comment_style):
    with pytest.raises(CommentStyleBadFormatException):
        CommentReader(comment_style)
