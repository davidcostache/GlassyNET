import logging
import discord
from discord.ext import commands
from bot.views import RoleView
from bot.bot_class import RoleManagerBot  # Import the custom bot class
from bot import messages  # Import messages


class Commands(commands.Cog):
    """
    A cog containing commands for managing roles and clearing messages.
    """

    def __init__(self, bot: RoleManagerBot) -> None:
        """
        Initializes the Commands cog with a bot instance.

        Args:
            bot (RoleManagerBot): The bot instance.
        """
        self.bot = bot

    @discord.app_commands.command(name="add", description="Add roles to a user.")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def add(self, interaction: discord.Interaction, user: discord.Member) -> None:
        """
        Adds specific roles to a user.

        Args:
            interaction (discord.Interaction): The interaction object.
            user (discord.Member): The user to whom roles will be added.
        """
        try:
            roles = [interaction.guild.get_role(role_id) for role_id in self.bot.role_to_channel.keys()]
            roles = [role for role in roles if role and role not in user.roles]

            if not roles:
                await interaction.response.send_message(messages.ROLE_ALREADY_HAVE_ALL, ephemeral=True)
                return

            view = RoleView(user, roles)
            await interaction.response.send_message(messages.SELECT_ROLES_TO_ADD, view=view, ephemeral=True)
        except Exception as e:
            logging.error(f"Error in add command: {e}")
            try:
                await interaction.followup.send(messages.ERROR_ADDING_ROLES, ephemeral=True)
            except discord.errors.NotFound:
                logging.error("Failed to send follow-up message: Interaction webhook not found.")

    @discord.app_commands.command(name="remove", description="Remove specific roles from a user.")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def remove(self, interaction: discord.Interaction, user: discord.Member) -> None:
        """
        Removes specific roles from a user.

        Args:
            interaction (discord.Interaction): The interaction object.
            user (discord.Member): The user from whom roles will be removed.
        """
        try:
            roles = [interaction.guild.get_role(role_id) for role_id in self.bot.role_to_channel.keys() if
                     interaction.guild.get_role(role_id) in user.roles]

            if not roles:
                await interaction.response.send_message(messages.USER_DOES_NOT_HAVE_ROLES, ephemeral=True)
                return

            view = RoleView(user, roles, remove=True)
            await interaction.response.send_message(messages.SELECT_ROLES_TO_REMOVE, view=view, ephemeral=True)
        except Exception as e:
            logging.error(f"Error in remove command: {e}")
            try:
                await interaction.followup.send(messages.ERROR_REMOVING_ROLES, ephemeral=True)
            except discord.errors.NotFound:
                logging.error("Failed to send follow-up message: Interaction webhook not found.")

    @discord.app_commands.command(name="clear", description="Clears a specified number of messages.")
    @discord.app_commands.checks.has_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction, amount: int) -> None:
        """
        Clears a specified number of messages from the channel.

        Args:
            interaction (discord.Interaction): The interaction object.
            amount (int): The number of messages to clear.
        """
        try:
            if amount <= 0:
                await interaction.response.send_message(
                    messages.SPECIFY_NUMBER_GREATER_THAN_ZERO, ephemeral=True
                )
                return

            await interaction.response.defer(ephemeral=True)
            deleted_messages = await interaction.channel.purge(limit=amount)
            number_of_messages = len(deleted_messages)
            message = "message" if number_of_messages == 1 else "messages"
            response = (f"Cleared {number_of_messages} {message}"
                        if deleted_messages else messages.NO_MESSAGES_TO_CLEAR)
            await interaction.followup.send(response, ephemeral=True)

        except discord.Forbidden:
            logging.error(messages.NO_PERMISSION_TO_DELETE_MESSAGES)
            try:
                await interaction.followup.send(messages.NO_PERMISSION_TO_DELETE_MESSAGES, ephemeral=True)
            except discord.errors.NotFound:
                logging.error("Failed to send follow-up message: Interaction webhook not found.")
        except discord.HTTPException as e:
            logging.error(f"Clear command: An error occurred: {e}")
            try:
                await interaction.followup.send(messages.ERROR_CLEARING_MESSAGES, ephemeral=True)
            except discord.errors.NotFound:
                logging.error("Failed to send follow-up message: Interaction webhook not found.")

    @discord.app_commands.command(name="verify", description="Learn how to verify your purchase.")
    async def verify(self, interaction: discord.Interaction) -> None:
        """
        Provides information on how to verify a purchase to users.

        Args:
            interaction (discord.Interaction): The interaction object.
        """
        try:
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(messages.VERIFICATION_INFO, ephemeral=True)
        except Exception as e:
            logging.error(f"Verify command: An error occurred: {e}")
            try:
                await interaction.followup.send(messages.ERROR_MODIFYING_ROLES, ephemeral=True)
            except discord.errors.NotFound:
                logging.error("Failed to send follow-up message: Interaction webhook not found.")
