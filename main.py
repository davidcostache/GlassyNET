import logging
import os
from dotenv import load_dotenv
import discord
from bot.bot_class import RoleManagerBot
from bot.commands import Commands


def main() -> None:
    """
    The main entry point for the bot application. Loads environment variables,
    initializes the bot, and runs it.
    """
    load_dotenv()  # Load environment variables from .env file
    intents = discord.Intents.all()
    bot = RoleManagerBot(command_prefix='/', intents=intents)

    @bot.event
    async def on_ready():
        logging.info("Bot is ready. Calling update_bot_activity and adding cogs.")
        await bot.update_bot_activity()
        await bot.add_cog(Commands(bot))
        await bot.tree.sync()
        logging.info(f"Logged in as {bot.user}")
        logging.info("Calling send_startup_message")
        await bot.send_startup_message()
        logging.info("Finished calling send_startup_message")
        logging.info("Starting periodic role check task")
        await bot.periodic_role_check()

    try:
        bot_token = os.getenv('DISCORD_TOKEN')
        if not bot_token:
            logging.error("DISCORD_TOKEN is not set in the environment variables")
            return
        bot.run(bot_token)
    except Exception as e:
        logging.error(f"Error running the bot: {e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    main()
