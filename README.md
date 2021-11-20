# Sir LionHeart
A discord bot that uses natural language processing to see if messages are derogatory. The bot doesn't delete messages with particular words, but rather looks at the context of the message.

## --Important--
To access trained model_file click here.

## Motivation
Cyberbullying is a huge threat to mental health and there aren't effective ways of combating it

Discord has a bot that attempts to solve this by deleting blacklisted words, but this method doesn't take the context of message into consideration. This makes the bot ban messages that aren’t derogatory, and also easy to bypass.

## How it Works
The bot intakes messages from the server, and sends it to the ML model The ML model predicts if the message is derogatory and sends the result back to the bot If the message is derogatory the bot uses our SQLITE database to add one to the amount of warnings for the author of the derogatory message. If the amount of warnings is greater than the tolerance, it either kicks or bans the user

## Advantages
The ML model uses fastText word embeddings to predict messages in split second time. It's difficult for users to bypass the bot No other discord bot has this feature Due to the use of natural language processing it is effective at detecting derogatory messages.
