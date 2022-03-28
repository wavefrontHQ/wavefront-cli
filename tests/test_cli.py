"""Tests for our main wave CLI module."""


import subprocess
import unittest

import wavefront_cli


class TestHelp(unittest.TestCase):
    """Test cases for wavefront cli."""

    def test_returns_usage_information(self):
        """Test wavefront cli help command."""
        output = subprocess.check_output(['wave', '-h']).decode()
        self.assertIn('Usage:', output)

        output = subprocess.check_output(['wave', '--help']).decode()
        self.assertIn('Usage:', output)


class TestVersion(unittest.TestCase):
    """Test cases for wavefront cli."""

    def test_returns_version_information(self):
        """Test wavefront cli version command."""
        output = subprocess.check_output(['wave', '--version']).decode()
        self.assertEqual(output.strip(), wavefront_cli.__version__)
