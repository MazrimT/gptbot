# gptbot
 
discord bot that takes prompts from user, asks chatgpt and replies the anwser to the user  
currently gpt-4 is not available (or at least I don't have it) through API so it's set to gpt-3.5-turbo
This was just a funny evening project, just for inspiration, probably won't do much more on it.

## install

### get discord token
sign up to: https://discord.com/developers/  
make a bot  
get the key

### get an openai account
sign up to: https://platform.openai.com/  
it's a paid service, not the same thing as chatGPT plus account
at the moment the cost for gpt-3.5-turbo is $0.002 / 1K tokens which is ~ 750 words.

### .env file
create an .env file in the root with following content:
```
DISCORD_TOKEN=your discord bot token here
OPENAI_API_KEY=your openai key here
```

### success?
publish the bot somewhere or run it on your own.
