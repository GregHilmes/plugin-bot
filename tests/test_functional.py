"""Functional tests for expected features.
"""

import unittest

import plugin_bot


class TestCanCreateBot(unittest.TestCase):
    """Tests for the most basic use cases."""
    def test_create_with_no_plugins(self):
        """Test that an empty bot can be created."""
        bot = plugin_bot.PluginBot([])
        self.assertEqual(bot.plugins, list())


if __name__ == '__main__':
    unittest.main()
