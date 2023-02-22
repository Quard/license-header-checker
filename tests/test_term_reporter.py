from unittest import mock

import termcolor

from license_header_checker.reporter import Resolution, TermReporter


def test_len():
    reporter = TermReporter()
    for i in range(5):
        reporter.add(f'fl_{i}.py', f'resolution {i}')
        assert len(reporter) == i + 1


def test_resolution_obj_on_add():
    reporter = TermReporter()

    assert reporter.files == []
    reporter.add('one.py', 'bad 1')
    two_resolution = Resolution('bad 2')
    reporter.add('two.py', two_resolution)

    assert len(reporter.files) == 2
    assert isinstance(reporter.files[0][1], Resolution)
    assert reporter.files[0][1] != two_resolution
    assert reporter.files[0][1].resolution == 'bad 1'
    assert reporter.files[1][1] == two_resolution


def test_resolution_no_header():
    resolution = TermReporter.resolution_no_header()

    assert isinstance(resolution, Resolution)
    assert resolution.resolution == 'header comment not found'
    assert resolution.details is None


def test_resolution_bad_license():
    resolution = TermReporter.resolution_bad_license('aabbb', 2)

    assert isinstance(resolution, Resolution)
    assert resolution.resolution == 'license has bad format'
    assert resolution.details == (
        termcolor.colored('aa', 'green')
        + termcolor.colored('bbb', 'red')
    )


def test_report():
    reporter = TermReporter()
    reporter.add('one.py', Resolution('aa', 'line one\nline two'))
    reporter.add('two.c', Resolution('not found'))
    with mock.patch('builtins.print') as m_print:
        reporter.report()

    m_print.assert_has_calls(
        (
            mock.call(termcolor.colored(reporter.files[0][1], 'yellow'), 'one.py'),
            mock.call('\tline one\n\tline two'),
            mock.call(termcolor.colored(reporter.files[1][1], 'yellow'), 'two.c'),
        ),
        any_order=False
    )
