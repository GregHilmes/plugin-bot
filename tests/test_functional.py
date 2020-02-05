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

            async def on_ready(self):
                TestPlugin.ready_calls += 1

        bot = plugin_bot.PluginBot([TestPlugin])
        self.assertIn(TestPlugin, bot.plugins)

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

            async def on_ready(self):
                """"""

        bot = plugin_bot.PluginBot([LoggingPlugin])

        # Run the bot
        await bot.login(TEST_TOKEN)
        try:
            with self.assertLogs(bot.logger, level='DEBUG') as cm:
                await asyncio.wait_for(bot.connect(), timeout=5)
        except asyncio.TimeoutError:
            await bot.close()

        self.assertIn('DEBUG:PluginBot:dispatching on_ready to LoggingPlugin',
                      cm.output)


if __name__ == '__main__':
    unittest.main()
