import discord
import pickle
import os


class Scoreboard:
	def __init__(self):
		self.scores = dict()

	async def loadData(self):
		if os.path.exists("score.txt"):
			score_file = open("score.txt", "rb")
			self.scores = pickle.load(score_file)

	async def saveData(self):
		score_file = open("score.txt", "wb")
		pickle.dump(self.scores, score_file)

	async def register(self, user_id):
		self.scores[user_id] = 0
		await self.saveData()

	async def add(self, user_id):
		self.scores[user_id] += 1
		await self.saveData()
	
	async def sub(self, user_id):
		self.scores[user_id] -= 1
		await self.saveData()

	async def printLeaderboard(self):
		s = "LEADERBOARD\n"
		for user_id, score in sorted(self.scores.items(), key=lambda x: x[1]):
			s += f"{bot.get_user(user_id).name} : {score}"
		return s

f = open("token.txt")
DISCORD_TOKEN = f.read()

scoreboard = Scoreboard()
scoreboard.loadData()

# GETS THE CLIENT OBJECT FROM DISCORD.PY. CLIENT IS SYNONYMOUS WITH BOT.
bot = discord.Client(intents=discord.Intents.all())

# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
	print("Ready!")


async def confirm(message):
	await message.add_reaction('👍')


# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	global scoreboard
	if message.channel.name == "scoreboard":
		if message.content == "!show":
			await message.channel.send(await scoreboard.printLeaderboard())
			await confirm(message)
		if message.content == "!register":
			await scoreboard.register(message.author.id)
			await scoreboard.saveData()
			await confirm(message)
		if message.content == "!add":
			await scoreboard.add(message.author.id)
			await scoreboard.saveData()
			await confirm(message)
		if message.content == "!sub":
			await scoreboard.sub(message.author.id)
			await scoreboard.saveData()
			await confirm(message)
		

# @bot.event
# async def on_reaction_add(reaction, user):
#     message = reaction.message # our embed
#     channel = discord.utils.get(message.guild.channels, name="welcome") #our channel
#     if message.channel.id == channel.id: # checking if it's the same channel
#         if message.author == bot.user: #checking if it's sent by the bot
#             if reaction.emoji.name == "👋🏽": #checking the emoji
#                 # enter code here, user is person that reacted

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)