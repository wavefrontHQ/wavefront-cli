"""Tests for our main wave CLI module."""


from subprocess import PIPE, Popen
from unittest import TestCase
from wave import __version__ as version


class TestHelp(TestCase):
    """Test cases for wavefront cli"""
    def test_returns_usage_information(self):
        """Test wavefront cli help command"""
        output = Popen(['wave', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)

        output = Popen(['wave', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue('Usage:' in output)


class TestVersion(TestCase):
    """Test cases for wavefront cli"""
    def test_returns_version_information(self):
        """Test wavefront cli version command"""
        output = Popen(['wave', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), version)
