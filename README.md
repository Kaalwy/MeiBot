# MeiBot

MeiBot is a powerful Discord bot designed to enhance your Discord server's experience. It offers various features, including music playback, dice rolling, RPG character creation, moderation tools, and more. If you'd like to contribute or collaborate on this project, feel free to reach out to me on Discord with the username `shusuiwy`.

## Features

- **Music Playback**: Stream music directly in voice channels from YouTube and local files.
- **Dice Rolling**: Roll various types of dice for gaming purposes with informative and fun responses.
- **RPG Features**: Create, customize, and manage RPG characters through interactive commands.
- **Moderation Tools**: Mute, unmute, kick, or ban users with documented commands.
- **Custom Command Prefix**: Use a custom prefix or mention the bot to trigger commands.

## RPG Features

- **RPG Character Creation**: Personalize your character through an interactive question system that adjusts attributes and abilities based on your choices, including classes and unique traits.
- **Character Status Check**: Check your character's stats and abilities anytime with a quick command.
- **Interactive Quiz for Skills**: Gain unique skills for your character based on responses to an interactive quiz, enriching the RPG experience.

## Getting Started

To get started with MeiBot, follow these simple steps:

### Prerequisites

Ensure you have Python 3.8 or higher installed. You can download it from [Python's official website](https://www.python.org/downloads/).

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Shusuiwy/MeiBot.git
    cd MeiBot
    ```

2. **.env required**:

    Create a .env file in the root of your project with the following contents:

    ```
    YOUR_TOKEN=your_discord_bot_token_here
    ```

3. **Install the requirements**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Test it!**

    ```bash
    python bot.py
    ```

## Usage

Once your bot is up and running, you can invite it to your Discord server using the OAuth2 URL generated from the Discord Developer Portal. Use the following command prefixes to interact with MeiBot:

### Music Commands:
- `.join` - Joins your voice channel.
- `.leave` - Leaves the voice channel.
- `.play <URL_or_MP3>` - Plays music from a URL or local file.
- `.stop` - Stops the music.
- `.skip` - Skips to the next song in the queue.

### Dice Commands:
- `.r <command>` - Rolls dice (e.g., .r d20, .roll 2d6+3).

### RPG Commands:
- `.caketale` - Initiates the character creation process for Caketale, with a question-based system that adjusts attributes and skills.
- `.status` - Displays the current status of your character, showing attributes and skills for easy reference during adventures.

### Moderation Commands:
- `.mute @user <duration>` - Silences a user for a specified duration.
- `.unmute @user` - Removes the mute from a user.
- `.ban @user <reason>` - Bans a user.
- `.kick @user <reason>` - Kicks a user from the server.

## Contributing

Contributions are welcome! If you'd like to work on MeiBot, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or fix.
- Make your changes.
- Submit a pull request with a clear description of your changes.

Alternatively, you can contact me via email or Discord at "kaalwy@proton.me".
