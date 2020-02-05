"""Module for the BasePlugin class, as well as basic plugin recipies.

"""
import logging


class BasePlugin:
    """A convenience class to inherit from when making plugins."""

    def __init_subclass__(cls, **kwargs):
        """Automatically create the unique logger object for the subclass.
        """
        cls.logger = logging.getLogger(f'PluginBot.{cls.__name__}')
