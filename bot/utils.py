import logging
import discord
from discord.ui import View, Select
from discord import SelectOption, Interaction


class RoleSelector(Select):
    """
    A UI element for selecting roles to add or remove from a user.
    """

    def __init__(self, user: discord.Member, roles: list[discord.Role], remove: bool = False):
        """
        Initializes the RoleSelector.

        Args:
            user (discord.Member): The user to whom roles are being added or removed.
            roles (list[discord.Role]): The list of roles to select from.
            remove (bool): Whether the selector is for removing roles. Defaults to False.
        """
        self.user = user
        self.roles = roles
        self.remove = remove

        options = [SelectOption(label=role.name, value=str(role.id)) for role in roles]
        placeholder = "Choose roles to add..." if not remove else "Choose specific roles to remove..."

        super().__init__(placeholder=placeholder, min_values=1, max_values=len(options), options=options)

    async def callback(self, interaction: Interaction):
        """
        Handles the callback when a role is selected.

        Args:
            interaction (Interaction): The interaction object.
        """
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
    """
    A UI view containing a RoleSelector for adding or removing roles.
    """

    def __init__(self, user: discord.Member, roles: list[discord.Role], remove: bool = False):
        """
        Initializes the RoleView.

        Args:
            user (discord.Member): The user to whom roles are being added or removed.
            roles (list[discord.Role]): The list of roles to select from.
            remove (bool): Whether the view is for removing roles. Defaults to False.
        """
        super().__init__()
        self.add_item(RoleSelector(user, roles, remove))
