# GlassyNET
## Overview

GlassyNET is a Discord bot designed to automate role management and user verification processes within Discord communities. Utilizing advanced integration with Discord's API, this bot enables seamless role assignment based on user actions or purchases, enhancing community interaction and management.

## Key Features

- **Automated Role Assignment**: Dynamically assigns roles to users, facilitating access control and personalized experiences based on user activities or transactions.
- **Purchase Verification**: Automates the process of verifying user purchases, sending customized notifications and granting access to resources or exclusive channels.
- **Role Management**: Provides tools for administrators to add or remove roles, maintaining an organized and secure environment for community interaction.
- **Continuous Operation**: Engineered for reliability, GlassyNET runs 24/7 on a VPS, utilizing systemd for resilience and uptime, ensuring consistent community support.

## Technical Implementation

Implemented in Python with the discord.py library, GlassyNET offers:

- Asynchronous handling for scalability and performance.
- Integration with Discord UI components for user-friendly interactions.
- Secure environment configuration via .env files.
- Comprehensive logging for maintenance and troubleshooting.

## Setup and Operation

Designed for self-hosting, setting up GlassyNET involves:

1. Cloning the repository.
2. Installing dependencies with `pip install -r requirements.txt`.
3. Configuring the `.env` file and script for bot tokens and role-channel mappings.

## Commands Overview

GlassyNET enhances community engagement through specialized commands:

- ### /clear
**Purpose**: Cleans up channel messages, maintaining a tidy communication space.

<img width="323" alt="Screenshot 2024-02-01 at 10 30 22 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/4b50f831-56bc-472c-8173-d989cacf593d">

- ### /add
**Purpose**: Assigns roles automatically, enriching the user experience by unlocking new content and channels based on criteria such as purchases or achievements.

<img width="815" alt="Screenshot 2024-02-01 at 10 31 57 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/7f767a85-917d-4e1b-9694-b936c52f7e5e">

- ### /remove
**Purpose**: Facilitates role management by allowing for the removal of access or privileges, ensuring community integrity.

<img width="815" alt="Screenshot 2024-02-01 at 10 32 51 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/15f1f5d6-144f-4729-803d-dd6ca4fc20f2">


- ### /verify
**Purpose**: Streamlines the verification process for new or existing members, enabling automated access to community benefits.

<img width="967" alt="Screenshot 2024-02-01 at 10 27 45 PM" src="https://github.com/davidcostache/GlassyNET/assets/136920495/f1277050-2cb2-4275-8144-05d617472747">

## Running GlassyNET

To deploy GlassyNET:

```
pip install -r requirements.txt
python main.py
```
Ensure a systemd service is configured for automatic bot recovery and stability.


## Contributions

Contributions are encouraged to enhance GlassyNET's capabilities. For feature suggestions or improvements, please open an issue or submit a pull request.

## License

GlassyNET is available under the MIT License. For more details, see the [LICENSE](LICENSE) file.

