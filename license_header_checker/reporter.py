# Copyright (c) 2023 Vadym Zakovinko
# SPDX-License-Identifier: MIT

import abc

import termcolor


class Resolution(abc.ABC):

    def __init__(self, resolution=None, details=None):
        self.resolution = resolution
        if self.resolution is None:
            self.resolution = self.MESSAGE

        self.details = details

    def __str__(self):
        return self.resolution


class ResolutionNoLicense(Resolution):
    MESSAGE = 'header comment not found'


class ResolutionAutoPopulatedLicense(Resolution):
    TERM_TEXT_COLOR = 'green'
    MESSAGE = 'license header not found, auto populated'


class ResolutionBadLicenseFormat(Resolution):
    MESSAGE = 'license has bad format'


class Reporter(abc.ABC):

    def __init__(self):
        self.files = []

    def add(self, filename, resolution):
        self.files.append((filename, resolution))

    @staticmethod
    def resolution_no_header():
        return ResolutionNoLicense()

    @staticmethod
    def resolution_bad_license(content, position):
        return ResolutionBadLicenseFormat(details=content)

    @staticmethod
    def resolution_auto_populated_license():
        return ResolutionAutoPopulatedLicense()

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
        return ResolutionNoLicense()

    @staticmethod
    def resolution_bad_license(content, position):
        return ResolutionBadLicenseFormat(
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
                termcolor.colored(resolution, getattr(resolution, 'TERM_TEXT_COLOR', 'yellow')),
                filename
            )
            if resolution.details:
                print('\n'.join(
                    f'\t{ln}'
                    for ln in resolution.details.split('\n')
                ))
