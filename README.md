# BigChungus
A garbage Discord bot for sending random files

## Usage
Create a Discord bot that can read, and send messages with attachments on https://discordapp.com/developers, add it to a server and replace the "<bot_token_goes_here>" at the bottom of the BigChungus Python script with the bot's token. Then start the bot and type "!here" in the channel you want the bot to send messages in. The commands are:
- !here: tells the bot in which channel to send messages in
- !category:rating: makes the bot send a random file from the given category/-ies (you can enter multiple categories separated by semicolons) and rating(s) ("sfw", "nsfw" or "all")

Then just put some files in the corresponding folders and you're good to go.

## Settings
The settings can be changed by clicking on the "Settings" button in the main window. Most things are self-explanatory but I think I have to say something about the dialog which opens when clicking "Auto". If you tick the box next to "Random?", you will have to enter two values in the text box separated by a semicolon, which will define the minimum and maximum delay between the automatically sent files (f.e. "0;0.1" would make the bot send a random file from the allowed categories each 0 to 0.1 minutes). If the box isn't ticked, you just have to enter a single value for the delay (also in minutes).
