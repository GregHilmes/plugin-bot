##########
Plugin Bot
##########

******************************************************
Making Discord bots with Python has never been easier.
******************************************************

=====
Usage
=====


>>> import plugin_bot
>>> class MyPlugin(plugin_bot.BasePlugin):
...     async def on_ready(client):
...         print('Ready to go!')
...
>>> discord_bot = plugin_bot.PluginBot([MyPlugin])
>>> discord_bot.run('PASS_TOKEN_HERE')

Obviously, this bot doesn't do much besides log in. It's the developer's responsibility to write/install/import plugins to be used. To see and example plugin, check out the docs or the basic plugins in ``plugin_bot.plugins`` (Coming soon).

You can add multiple plugins in the list passed to the ``PluginBot`` constructor, and each Discord event will be dispatched to all plugins. This creates a greater degree of code reuse and modularity.

=============
Security Note
=============
Don't ever store your login token in source code or allow it into version control. Use an environment variable instead, or load the token from a file.
