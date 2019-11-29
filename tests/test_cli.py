"""Tests for our main wave CLI module."""


from subprocess import PIPE, Popen
from unittest import TestCase
from wave import __version__ as version


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = Popen(['wave', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)

        output = Popen(['wave', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = Popen(['wave', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), version)
