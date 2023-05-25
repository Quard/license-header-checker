from datetime import date
from io import StringIO

import pytest

from license_header_checker.exceptions import CommentStyleBadFormatException
from license_header_checker.writer import LicenseWriter


def test_populate_license_single_line_comment():
    tmpl = StringIO('test license\n\nheader')
    src_file = StringIO('from datetime import datetime\n\nprint(datetime.now())')

    LicenseWriter('#', tmpl).write(src_file)

    src_file.seek(0)
    assert src_file.read() == (
        '# test license\n#\n# header\n\n'
        'from datetime import datetime\n\nprint(datetime.now())'
    )


def test_populate_license_multi_line_comment():
    tmpl = StringIO('test license\nheader')
    src_file = StringIO('#include <stdio.h>\n\nvoid main(void) {\n  printf("Hello")\n}')

    LicenseWriter('/*| *| */', tmpl).write(src_file)

    src_file.seek(0)
    assert src_file.read() == (
        '/*\n * test license\n * header\n */\n\n'
        '#include <stdio.h>\n\nvoid main(void) {\n  printf("Hello")\n}'
    )


@pytest.mark.parametrize(
    ('tmpl', 'expected_line_end'),
    (
        ('1\n2\n', '\n'),
        ('1\r\n2', '\r\n'),
        ('123', '\n'),        # default value
    )
)
def test_detect_line_end(tmpl, expected_line_end):
    writer = LicenseWriter('#', StringIO(tmpl))
    assert writer._get_line_end(writer._get_template()) == expected_line_end


def test_year_substitution():
    tmpl = StringIO("Hello {YEAR}!")
    writer = LicenseWriter('#', tmpl)

    assert writer._get_template() == f'Hello {date.today().year}!'


@pytest.mark.parametrize(
    ('comment_style', ),
    (
        ('|', ),
        ('|||', ),
    )
)
def test_comment_style_bad_format(comment_style):
    with pytest.raises(CommentStyleBadFormatException):
        LicenseWriter(comment_style, StringIO(''))
