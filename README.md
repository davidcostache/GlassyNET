# GlassyNET
## Overview

This Discord bot was developed to facilitate role management within my Minecraft community, which I've been proudly co-founding and administering for several years alongside a friend. The primary function of this bot is to automatically assign roles to users who have purchased our Minecraft plugins and to notify them accordingly. This automation significantly enhances our community management by streamlining the verification and role assignment processes.

## Features

- **Role Assignment**: Automatically assigns roles based on the purchases made by community members. This feature is crucial for managing access to specific channels dedicated to our Minecraft plugins.
- **Purchase Verification**: Sends personalized verification messages to users, thanking them for their purchases and providing them with information on how to access their purchased plugins.
- **Role Removal and Message Deletion**: Offers administrators the ability to remove roles and clear messages within channels, ensuring effective moderation and channel maintenance.
- **24/7 Operation**: The bot operates continuously on a VPS hosted on Ubuntu. It's kept running using systemd, ensuring constant availability to manage roles and respond to user actions without downtime.

## Implementation Details

The bot is implemented in Python, utilizing the discord.py library to interact with the Discord API. Key features include:

- Asynchronous event handling for efficient operation under varying loads.
- Integration with Discord's UI components (e.g., View, Select) for interactive role selection.
- Use of environment variables for secure token management, facilitated by the dotenv package.
- Logging for debugging and monitoring the bot's operation.

## Setup and Usage

The bot is designed to be self-hosted on a VPS or similar environment. Setup involves cloning the repository, installing dependencies via pip, and configuring the bot token and role-channel mappings in .env and the script file, respectively.

## Command Descriptions

Enhance your Discord community management with these specialized commands:

### /clear Command
- **Action**: Deletes a specified number of messages from a channel.
- **Benefit**: Keeps channels clean and free of spam or outdated messages, facilitating a better conversation flow.
- **Usage**: Ideal for moderators who need to maintain order and clarity in community discussions.
- **Screenshot**:

<img width="323" alt="Screenshot 2024-02-01 at 10 30 22 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/4b50f831-56bc-472c-8173-d989cacf593d">

### /add Command
- **Action**: Assigns designated roles to users, automatically or upon request.
- **Benefit**: Streamlines access to exclusive channels and content, based on user activity or purchases, enhancing community engagement.
- **Usage**: Useful for rewarding community members, granting access to special roles, or unlocking premium content.
- **Screenshot**:

<img width="815" alt="Screenshot 2024-02-01 at 10 31 57 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/7f767a85-917d-4e1b-9694-b936c52f7e5e">


### /remove Command
- **Action**: Removes specific roles from a user, either manually by an administrator or through an automated process.
- **Benefit**: Allows for dynamic role management, ensuring that access rights are current and reflect the user's status in the community.
- **Usage**: Essential for revoking access when necessary or managing role transitions smoothly.
- **Screenshot**:

<img width="815" alt="Screenshot 2024-02-01 at 10 32 51 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/15f1f5d6-144f-4729-803d-dd6ca4fc20f2">


### /verify Command
- **Action**: Provides users with instructions or automates the verification process for accessing certain community benefits.
- **Benefit**: Simplifies the process of verifying purchases or membership statuses, ensuring users can quickly access their entitlements.
- **Usage**: Key for communities that offer premium content or services, streamlining the onboarding of new members.
- **Screenshot**:
<img width="967" alt="Screenshot 2024-02-01 at 10 27 45 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/f1277050-2cb2-4275-8144-05d617472747">


Each command is crafted to address specific administrative needs, ensuring that community leaders can manage members efficiently and effectively.



## Running the Bot

To run the bot, ensure that Python 3.8 or newer is installed on your system, along with the required packages:
```
pip install -r requirements.txt
```
Then, start the bot using:
```
python main.py
```

Ensure that the systemd service is configured to restart the bot automatically in case of a crash or system reboot.


## Contributions

Feedback and contributions are welcome! If you're interested in improving the bot or suggesting new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

