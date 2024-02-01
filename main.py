import asyncio
import logging
import os
import discord
from discord import Interaction, SelectOption
from discord.ext import commands
from discord.ui import View, Select
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

# Set up the bot with command prefix and intents
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Mapping of role IDs to channel IDs for role-specific channels
role_to_channel = {
    380725404262072320: "1200047665442979860",
    393044988411379742: "1195736480950276196",
    380725142608674816: "1195734262792605846",
    380724874236395520: "1195452480687964344"
}

# Queue for role updates to process role assignments asynchronously
role_update_queue = {}


# noinspection PyUnresolvedReferences
class Commands(commands.Cog):
    """Defines a set of commands for managing roles and messages in a Discord server."""
    def __init__(self, bot_instance):
        """Initializes the commands with a bot instance."""
        self.bot = bot_instance

    @discord.app_commands.command(name="add", description="Add roles to a user.")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        """Allows administrators to add specific roles to a user."""
        try:
            roles = [interaction.guild.get_role(role_id) for role_id in role_to_channel.keys()]
            roles = [role for role in roles if role and role not in user.roles]

            if not roles:
                await interaction.response.send_message("This user already has all the roles.", ephemeral=True)
                return

            view = RoleView(user, roles)
            await interaction.response.send_message("Select roles to add:", view=view, ephemeral=True)
        except Exception as e:
            logging.error(f"Error in add command: {e}")
            await interaction.response.send_message("An error occurred while adding roles.", ephemeral=True)

    @discord.app_commands.command(name="remove", description="Remove specific roles from a user.")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        """Allows administrators to remove specific roles from a user."""
        try:
            roles = [interaction.guild.get_role(role_id) for role_id in role_to_channel.keys() if
                     interaction.guild.get_role(role_id) in user.roles]

            if not roles:
                await interaction.response.send_message("This user does not have any of the specific roles to remove.",
                                                        ephemeral=True)
                return

            view = RoleView(user, roles, remove=True)
            await interaction.response.send_message("Select specific roles to remove:", view=view, ephemeral=True)
        except Exception as e:
            logging.error(f"Error in remove command: {e}")
            await interaction.response.send_message("An error occurred while removing roles.", ephemeral=True)

    @discord.app_commands.command(name="clear", description="Clears a specified number of messages.")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Allows administrators to clear a specified number of messages from a channel."""
        try:
            if amount <= 0:
                await interaction.response.send_message(
                    "Please specify a number greater than 0.", ephemeral=True
                )
                return

            await interaction.response.defer(ephemeral=True)
            deleted_messages = await interaction.channel.purge(limit=amount)
            number_of_messages = len(deleted_messages)
            message = "message" if number_of_messages == 1 else "messages"
            response = (f"Cleared {number_of_messages} {message}"
                        if deleted_messages else "There were no messages to clear.")
            await interaction.followup.send(response, ephemeral=True)

        except discord.Forbidden:
            logging.error("Clear command: Bot does not have permission to delete messages in this channel.")
            await interaction.followup.send("I do not have permission to delete messages in this channel.",
                                            ephemeral=True)
        except discord.HTTPException as e:
            logging.error(f"Clear command: An error occurred: {e}")
            await interaction.followup.send("An error occurred while trying to clear messages.", ephemeral=True)

    @discord.app_commands.command(name="verify", description="Learn how to verify your purchase.")
    async def verify(self, interaction: discord.Interaction):
        """Provides information on how to verify a purchase to users."""
        try:
            await interaction.response.defer(ephemeral=True)
            response = ("For more details on how to verify your purchase, "
                        "please visit the **Verification** section in the <id:home> "
                        "for further information.")
            await interaction.followup.send(response, ephemeral=True)

        except Exception as e:
            logging.error(f"Verify command: An error occurred: {e}")
            await interaction.followup.send("An error occurred while providing verification information.",
                                            ephemeral=True)


# noinspection PyUnresolvedReferences
class RoleSelector(Select):
    """A UI element for selecting roles to add or remove from a user."""
    def __init__(self, user, roles, remove=False):
        self.user = user
        self.roles = roles
        self.remove = remove

        if remove:
            options = [SelectOption(label=role.name, value=str(role.id)) for role in roles]
            placeholder = "Choose specific roles to remove..."
        else:
            options = [SelectOption(label=role.name, value=str(role.id)) for role in roles if role not in user.roles]
            placeholder = "Choose roles to add..."

        super().__init__(placeholder=placeholder, min_values=1, max_values=len(options), options=options)

    async def callback(self, interaction: Interaction):
        try:
            if self.remove:
                roles_to_modify = [interaction.guild.get_role(int(role_id)) for role_id in self.values]
                await self.user.remove_roles(*roles_to_modify)
                await interaction.response.send_message(f"Roles removed for {self.user.mention}", ephemeral=True)
            else:
                for role_id in self.values:
                    role = interaction.guild.get_role(int(role_id))
                    await self.user.add_roles(role)
                await interaction.response.send_message(f"Roles added for {self.user.mention}", ephemeral=True)

        except discord.Forbidden:
            logging.error(f"RoleSelector callback: Bot lacks permissions to modify roles for {self.user}")
            await interaction.response.send_message("I don't have permission to modify these roles.", ephemeral=True)
        except discord.HTTPException as e:
            logging.error(f"RoleSelector callback: HTTP error occurred: {e}")
            await interaction.response.send_message("An error occurred while modifying roles.", ephemeral=True)
        except Exception as e:
            logging.error(f"RoleSelector callback: Unexpected error: {e}")
            await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)


class RoleView(View):
    """A UI view containing a RoleSelector for adding or removing roles."""
    def __init__(self, user, roles, remove=False):
        super().__init__()
        self.add_item(RoleSelector(user, roles, remove))


@bot.event
async def on_ready():
    """Event handler called when the bot is ready."""
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over the server"))
    await bot.add_cog(Commands(bot))
    await bot.tree.sync()
    await bot.loop.create_task(periodic_role_check())


async def send_verification_message(member, roles):
    """Sends a verification message to a newly verified member."""
    channel_id = 1200460467622137936
    channel = bot.get_channel(channel_id)
    role_list = list(roles)

    if not channel:
        print("Verification channel not found.")
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
            asyncio.ensure_future(delete_message_after_delay(message))

    except discord.HTTPException as e:
        print(f"Failed to send verification message: {e}")


async def delete_message_after_delay(message):
    """Deletes a message after a specified delay."""
    await asyncio.sleep(86400)  # Wait for 24 hours
    try:
        await message.delete()
    except discord.NotFound:
        pass  # Message was already deleted
    except discord.Forbidden:
        print(f"Bot does not have permission to delete message: {message.id}")
    except discord.HTTPException as e:
        print(f"Error occurred while deleting message: {e}")


async def process_role_queue(member):
    """Processes queued role updates for a member."""
    await asyncio.sleep(5)
    roles = role_update_queue.pop(member.id, [])
    if roles:
        await send_verification_message(member, set(roles))


@bot.event
async def on_member_update(before, after):
    """Event handler for when a member's roles are updated."""
    try:
        new_roles = set(after.roles) - set(before.roles)
        added_roles = [role for role in new_roles if role.id in role_to_channel.keys()]

        if added_roles:
            queued_roles = role_update_queue.get(after.id, [])
            unique_roles = [role for role in added_roles if role not in queued_roles]

            if unique_roles:
                role_update_queue.setdefault(after.id, []).extend(unique_roles)
                if len(queued_roles) == 0:
                    await asyncio.create_task(process_role_queue(after))
    except Exception as e:
        print(f"Error in on_member_update: {e}")


async def assign_role_to_member(member, role_id):
    """Assigns a specified role to a member."""
    excluded_member_ids = [1200196215481041018, 1086954578764902481, 189771862610411524]

    if member.id in excluded_member_ids:
        return

    role = member.guild.get_role(role_id)
    if not role:
        print(f"Role with ID {role_id} not found.")
        return

    if role not in member.roles:
        try:
            await member.add_roles(role)
            print(f"Role {role.name} has been added to {member.name}.")
        except Exception as e:
            print(f"Error assigning role to {member.name}: {e}")


@bot.event
async def on_member_join(member):
    """Event handler for when a new member joins the server."""
    role_id = 372378135557308427
    await assign_role_to_member(member, role_id)


async def check_and_assign_role(guild, role_id):
    """Checks and assigns a role to all members of a guild."""
    role = guild.get_role(role_id)
    if not role:
        print(f"Role with ID {role_id} not found.")
        return

    limit = 1000
    after = None

    while True:
        members = []
        async for member in guild.fetch_members(limit=limit, after=after):
            members.append(member)
            await assign_role_to_member(member, role_id)

        if len(members) < limit:
            break

        after = members[-1]

    print("Finished assigning roles to all members.")


async def periodic_role_check():
    """Periodically checks and assigns roles to members in the guild."""
    await bot.wait_until_ready()
    guild_id = 372369352173027331
    while not bot.is_closed():
        guild = bot.get_guild(guild_id)
        if guild:
            await check_and_assign_role(guild, 372378135557308427)
        await asyncio.sleep(43200)

# Load the .env file and run the bot
load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))