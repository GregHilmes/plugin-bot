"""Plugin Bot - a Discord client designed to be used plug-n-play style.
"""
import functools
import logging

import discord


class PluginBot(discord.Client):
    """Represents a Discord client that is easily adaptable through plugins."""
    def __init__(self, plugins):
        """Create a bot with the plugins passed."""
        super(PluginBot, self).__init__()
        self.plugins = plugins
        self.logger = logging.getLogger(self.__class__.__name__)

    def dispatch(self, event, *args, **kwargs):
        super(PluginBot, self).dispatch(event, *args, **kwargs)

        method = 'on_' + event

        for plugin in self.plugins:
            if hasattr(plugin, method):
                self.logger.debug('dispatching %s to %s', method,
                                  plugin.__name__)
                coro = functools.partial(getattr(plugin, method), self)
                self._schedule_event(coro, method, *args, **kwargs)
