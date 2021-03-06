"""Functional tests for expected features.
"""
import asyncio
import os
import unittest

import plugin_bot

TEST_TOKEN = os.environ.get('DISCORD_TEST_TOKEN')


class TestCanCreateBot(unittest.IsolatedAsyncioTestCase):
    """Tests for the most basic use cases."""
    def test_create_with_no_plugins(self):
        """Test that an empty bot can be created."""
        bot = plugin_bot.PluginBot([])
        self.assertEqual(bot.plugins, list())

    async def test_create_with_mock_plugin(self):
        """Test that a basic plugin is used."""
        class TestPlugin:
            ready_calls = 0

            async def on_ready(self, client):
                TestPlugin.ready_calls += 1

        plugin = TestPlugin()

        bot = plugin_bot.PluginBot([plugin])
        self.assertIn(plugin, bot.plugins)

        # Run the bot
        await bot.login(TEST_TOKEN)
        try:
            await asyncio.wait_for(bot.connect(), timeout=5)
        except asyncio.TimeoutError:
            await bot.close()

        self.assertNotEqual(TestPlugin.ready_calls, 0, 'on_ready not called')

    async def test_logs_dispatching_events(self):
        """Test that the bot logs whenever a plugin event is dispatched.
        """
        class LoggingPlugin:

            async def on_ready(self, client):
                """"""

        bot = plugin_bot.PluginBot([LoggingPlugin()])

        # Run the bot
        await bot.login(TEST_TOKEN)
        try:
            with self.assertLogs(bot.logger, level='DEBUG') as cm:
                await asyncio.wait_for(bot.connect(), timeout=5)
        except asyncio.TimeoutError:
            await bot.close()

        self.assertIn('DEBUG:PluginBot:dispatching on_ready to LoggingPlugin',
                      cm.output)


class TestCanCreatePlugin(unittest.TestCase):
    """Test that a user can inherit and create their own plugin classes."""
    def test_can_inherit(self):
        """Test that a user plugin properly inherits BasePlugin.
        """
        class MyCoolPlugin(plugin_bot.BasePlugin):
            """"""

        self.assertTrue(issubclass(MyCoolPlugin, plugin_bot.BasePlugin))
        self.assertTrue(hasattr(MyCoolPlugin, 'logger'))
        self.assertEqual(MyCoolPlugin.logger.name, 'PluginBot.MyCoolPlugin')


if __name__ == '__main__':
    unittest.main()
