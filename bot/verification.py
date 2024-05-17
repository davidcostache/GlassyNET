import asyncio
import logging
from datetime import datetime, timedelta, timezone
import discord


async def send_verification_message(bot: discord.Client, member: discord.Member, roles: set[discord.Role],
                                    role_to_channel: dict[int, str]) -> None:
    """
    Sends a verification message to a newly verified member.

    Args:
        bot (discord.Client): The bot instance.
        member (discord.Member): The member to whom the verification message is sent.
        roles (set[discord.Role]): The roles assigned to the member.
        role_to_channel (dict[int, str]): Mapping of role IDs to channel IDs.
    """
    channel_id = 1200460467622137936
    channel = bot.get_channel(channel_id)
    role_list = list(roles)

    if not channel:
        logging.error("Verification channel not found.")
        return

    try:
        if channel:
            embed = discord.Embed(
                title="Thank you for your purchase!",
                color=discord.Color(0x059669)
            )
            embed.set_thumbnail(url=member.avatar.url)

            role_names = [role.name for role in role_list]
            role_mentions = [
                f"<#{role_to_channel.get(role.id)}>" for role in role_list
                if role.id in role_to_channel
            ]

            if len(role_list) == 1:
                roles_text = f"**{role_names[0]}**"
                plugin_text = "plugin"
                topic_text = "the post below"
            else:
                roles_text = ", ".join([f"**{name}**" for name in role_names[:-1]])
                roles_text += f" and **{role_names[-1]}**"
                plugin_text = "plugins"
                topic_text = "the posts below"

            embed.description = (
                f"You have been successfully verified for {roles_text}. "
                f"For complete documentation of the {plugin_text}, please access {topic_text}."
            )

            for role_name, role_mention in zip(role_names, role_mentions):
                embed.add_field(name=role_name, value=role_mention, inline=True)

            deletion_time = datetime.now(timezone.utc) + timedelta(hours=24)
            embed.set_footer(
                text=f"This message will be deleted in 24 hours ({deletion_time.strftime('%Y-%m-%d %H:%M:%S')} UTC)"
            )

            message = await channel.send(content=member.mention, embed=embed)
            asyncio.create_task(delete_message_after_delay(message))  # noqa

    except discord.HTTPException as e:
        logging.error(f"Failed to send verification message: {e}")


async def delete_message_after_delay(message: discord.Message) -> None:
    """
    Deletes a message after a 24-hour delay.

    Args:
        message (discord.Message): The message to be deleted.
    """
    await asyncio.sleep(86400)
    try:
        await message.delete()
    except discord.NotFound:
        pass
    except discord.Forbidden:
        logging.error(f"Bot lacks permission to delete message: {message.id}")
    except discord.HTTPException as e:
        logging.error(f"Error occurred while deleting message: {e}")
