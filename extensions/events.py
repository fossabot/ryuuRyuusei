import re
from time import time

import interactions as ipy
from interactions.api.events import CommandError

from modules.const import EMOJI_FORBIDDEN


class BotEvents(ipy.Extension):
    @ipy.listen(disable_default_listeners=True)
    async def on_command_error(self, event: CommandError):
        """Handle command errors"""
        if isinstance(event.error, ipy.errors.CommandOnCooldown):
            emoji_id = re.search(r"<a?:\w+:(\d+)>", EMOJI_FORBIDDEN).group(1)
            now = time()
            remaining = now + event.error.cooldown.get_cooldown_time()
            embed = ipy.Embed(
                author=ipy.EmbedAuthor(
                    name="Forbidden action",
                ),
                title="You are on cooldown",
                description=f"Try again <t:{int(remaining)}:R>",
                color=0xFF0000,
            )
            embed.set_thumbnail(
                url=f"https://cdn.discordapp.com/emojis/{emoji_id}.webp"
            )
            await event.ctx.send(embed=embed, ephemeral=True)
        else:
            await self.bot.on_command_error(self.bot, event)


def setup(bot):
    BotEvents(bot)
