# Copyright (c) 2023 Vadym Zakovinko
# SPDX-License-Identifier: MIT

import abc

import termcolor


class Resolution:

    def __init__(self, resolution, details=None):
        self.resolution = resolution
        self.details = details

    def __str__(self):
        return self.resolution


class Reporter(abc.ABC):

    def __init__(self):
        self.files = []

    def add(self, filename, resolution):
        self.files.append((filename, resolution))

    @staticmethod
    def resolution_no_header():
        return Resolution('header comment not found')

    @staticmethod
    def resolution_bad_license(content, position):
        return Resolution('license has bad format', details=content)

    def __len__(self):
        return len(self.files)

    @abc.abstractmethod
    def report(self):
        pass


class TermReporter(Reporter):

    def __init__(self):
        self.files = []

    def add(self, filename, resolution):
        if not isinstance(resolution, Resolution):
            resolution = Resolution(resolution)
        self.files.append((filename, resolution))

    @staticmethod
    def resolution_no_header():
        return Resolution('header comment not found')

    @staticmethod
    def resolution_bad_license(content, position):
        return Resolution(
            'license has bad format',
            details=(
                termcolor.colored(content[:position], 'green')
                + termcolor.colored(content[position:], 'red')
            )
        )

    def __len__(self):
        return len(self.files)

    def report(self):
        for filename, resolution in self.files:
            print(
                termcolor.colored(resolution, 'yellow'),
                filename
            )
            if resolution.details:
                print('\n'.join(
                    f'\t{ln}'
                    for ln in resolution.details.split('\n')
                ))
