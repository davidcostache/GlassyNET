import asyncio
import logging
import discord
from discord.ext import commands
from bot.verification import send_verification_message
from bot import messages  # Import messages


class RoleManagerBot(commands.Bot):
    """
    A custom bot class inheriting from commands.Bot, tailored for managing roles in a Discord server.
    """

    def __init__(self, command_prefix: str, intents: discord.Intents) -> None:
        """
        Initializes the RoleManagerBot with specified command prefix and intents.

        Args:
            command_prefix (str): The prefix for bot commands.
            intents (discord.Intents): The intents for the bot.
        """
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.role_to_channel: dict[int, str] = {
            380725404262072320: "1200047665442979860",
            393044988411379742: "1195736480950276196",
            380725142608674816: "1195734262792605846",
            380724874236395520: "1195452480687964344"
        }
        self.role_update_queue: dict[int, list[discord.Role]] = {}
        self.startup_channel_id: int = 1094604434195107921

    async def send_startup_message(self) -> None:
        """
        Sends a startup message to a specific channel when the bot starts.
        """
        logging.info("Attempting to send startup message")
        await asyncio.sleep(1)
        logging.info("Fetching startup channel")
        startup_channel = self.get_channel(self.startup_channel_id)
        logging.info(f"Startup channel: {startup_channel}")
        if startup_channel:
            logging.info(f"Startup channel found: {startup_channel.id}")
            try:
                await startup_channel.send(messages.STARTUP_MESSAGE)
                logging.info("Startup message sent successfully")
            except Exception as e:
                logging.error(f"Failed to send startup message: {e}")
        else:
            logging.warning("Startup channel not found")

    async def send_shutdown_message(self) -> None:
        """
        Sends a shutdown message to a specific channel when the bot is shutting down.
        """
        logging.info("Bot is shutting down. Fetching shutdown channel.")
        shutdown_channel = self.get_channel(self.startup_channel_id)
        if shutdown_channel:
            try:
                await shutdown_channel.send(messages.SHUTDOWN_MESSAGE)
                logging.info("Shutdown message sent successfully")
            except Exception as e:
                logging.error(f"Failed to send shutdown message: {e}")
        else:
            logging.warning("Shutdown channel not found")

    async def close(self) -> None:
        """
        Closes the bot and its resources.
        """
        logging.info("Closing bot and resources")
        await self.send_shutdown_message()
        await self.close_http_session()
        await super().close()

    async def close_http_session(self) -> None:
        """
        Closes the bot's HTTP session.
        """
        if self.http and self.http.connector:
            await self.http.connector.close()
            logging.info("HTTP session closed")

    async def update_bot_activity(self) -> None:
        """
        Updates the bot's activity to display the number of members in the server.
        """
        logging.info("Updating bot activity")
        guild = self.guilds[0]
        logging.info(f"Selected guild: {guild.name}")
        member_count = guild.member_count
        activity_text = f"over {member_count:,} members"
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_text))
        logging.info("Bot activity updated")

    @staticmethod
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
            logging.warning("Message already deleted.")
        except discord.Forbidden:
            logging.error(f"Bot lacks permission to delete message: {message.id}")
        except discord.HTTPException as e:
            logging.error(f"Error occurred while deleting message: {e}")

    async def process_role_queue(self, member: discord.Member) -> None:
        """
        Processes the role update queue for a member.

        Args:
            member (discord.Member): The member whose roles are being processed.
        """
        await asyncio.sleep(5)
        roles = self.role_update_queue.pop(member.id, [])
        if roles:
            await send_verification_message(self, member, set(roles), self.role_to_channel)

    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        """
        Handles updates to a member's roles.

        Args:
            before (discord.Member): The member before the update.
            after (discord.Member): The member after the update.
        """
        try:
            new_roles = set(after.roles) - set(before.roles)
            added_roles = [role for role in new_roles if role.id in self.role_to_channel.keys()]

            if added_roles:
                queued_roles = self.role_update_queue.get(after.id, [])
                unique_roles = [role for role in added_roles if role not in queued_roles]

                if unique_roles:
                    self.role_update_queue.setdefault(after.id, []).extend(unique_roles)
                    if len(queued_roles) == 0:
                        await asyncio.create_task(self.process_role_queue(after))
        except Exception as e:
            logging.error(f"Error in on_member_update: {e}")

    @staticmethod
    async def assign_role_to_member(member: discord.Member, role_id: int) -> None:
        """
        Assigns a role to a member.

        Args:
            member (discord.Member): The member to whom the role will be assigned.
            role_id (int): The ID of the role to be assigned.
        """
        excluded_member_ids = [1200196215481041018, 1086954578764902481, 189771862610411524]

        if member.id in excluded_member_ids:
            return

        role = member.guild.get_role(role_id)
        if not role:
            logging.error(f"Role with ID {role_id} not found.")
            return

        if role not in member.roles:
            try:
                await member.add_roles(role)
                logging.info(f"Role {role.name} has been added to {member.name}.")
            except Exception as e:
                logging.error(f"Error assigning role to {member.name}: {e}")

    async def on_member_join(self, member: discord.Member) -> None:
        """
        Handles a new member joining the server.

        Args:
            member (discord.Member): The member who joined.
        """
        role_id = 372378135557308427
        await self.assign_role_to_member(member, role_id)
        await self.update_bot_activity()

    async def on_member_remove(self, member: discord.Member) -> None:
        """
        Handles a member leaving the server.

        Args:
            member (discord.Member): The member who left.
        """
        await self.update_bot_activity()

    async def check_and_assign_role(self, guild: discord.Guild, role_id: int) -> None:
        """
        Checks and assigns a role to all members in the guild.

        Args:
            guild (discord.Guild): The guild in which to assign roles.
            role_id (int): The ID of the role to assign.
        """
        role = guild.get_role(role_id)
        if not role:
            logging.error(f"Role with ID {role_id} not found.")
            return

        limit = 1000
        after = None

        while True:
            members = []
            async for member in guild.fetch_members(limit=limit, after=after):
                members.append(member)
                await self.assign_role_to_member(member, role_id)

            if len(members) < limit:
                break

            after = members[-1]

        logging.info("Finished assigning roles to all members.")

    async def periodic_role_check(self) -> None:
        """
        Periodically checks and assigns roles to members in the guild.
        """
        await self.wait_until_ready()
        guild_id = 372369352173027331
        while not self.is_closed():
            guild = self.get_guild(guild_id)
            if guild:
                await self.check_and_assign_role(guild, 372378135557308427)
            await asyncio.sleep(43200)
