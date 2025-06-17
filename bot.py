import discord
import random
import smtplib
from email.mime.text import MIMEText
import psycopg2
from datetime import datetime, timedelta

from config import (
    DISCORD_TOKEN, SMTP_EMAIL, SMTP_PASSWORD, GUILD_ID,
    DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
)

# Discord bot setup
intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True
bot = discord.Client(intents=intents)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cur = conn.cursor()

def send_otp_email(email, otp):
    msg = MIMEText(f"Your Algopath verification OTP is: {otp}")
    msg['Subject'] = 'Algopath OTP'
    msg['From'] = SMTP_EMAIL
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, email, msg.as_string())

@bot.event
async def on_ready():
    print("\u2705 Bot is ready.")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_member_join(member):
    try:
        await member.send("\ud83d\udc4b Welcome to Algopath! Please enter your registered Algopath email to start verification.")
    except discord.Forbidden:
        print(f"\u274c Couldn’t DM {member.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user = message.author
    content = message.content.strip()

    # Doubt handling in #doubts channel
    if message.guild and message.channel.name == "doubts":
        if message.reference:  # Check if it's a reply
            replied_to_id = message.reference.message_id
            cur.execute("SELECT id, user_id FROM doubts WHERE message_id = %s", (replied_to_id,))
            row = cur.fetchone()
            if row and row[1] == user.id and content.lower() == "resolved":
                cur.execute("UPDATE doubts SET resolved = TRUE WHERE id = %s", (row[0],))
                conn.commit()
                await message.channel.send(f"\u2705 Your doubt has been marked as resolved, {user.name}.")
                return
        else:
            cur.execute(
                "INSERT INTO doubts (user_id, username, doubt, message_id) VALUES (%s, %s, %s, %s)",
                (user.id, user.name, content, message.id)
            )
            conn.commit()
            prompt = await message.channel.send(
                f"\ud83d\udccc Please reply to *your message* with 'resolved' once your doubt has been cleared, {user.name}."
            )
            return

    # Email + OTP logic via DM
    if isinstance(message.channel, discord.DMChannel):
        if '@' in content and '.' in content:
            cur.execute("SELECT * FROM emails WHERE email = %s", (content,))
            if not cur.fetchone():
                await message.channel.send("\u274c Email not found in database.")
                return

            cur.execute("SELECT * FROM verified_users WHERE email = %s", (content,))
            if cur.fetchone():
                await message.channel.send("\u26a0\ufe0f This email has already been used for verification.")
                return

            otp = str(random.randint(100000, 999999))
            cur.execute("INSERT INTO otps (email, otp) VALUES (%s, %s)", (content, otp))
            conn.commit()
            send_otp_email(content, otp)
            await message.channel.send("\ud83d\udce7 OTP sent to your email. Enter it here to complete verification.")

        elif content.isdigit():
            cur.execute("SELECT email, created_at FROM otps WHERE otp=%s", (content,))
            result = cur.fetchone()
            if result:
                email, created_at = result
                if datetime.now() - created_at < timedelta(minutes=10):
                    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
                    role = discord.utils.get(guild.roles, name='Verified')
                    member = guild.get_member(user.id)

                    if role and member:
                        await member.add_roles(role)
                        await message.channel.send("\ud83c\udf89 Verification complete! Welcome to Algopath.")
                        print(f"\u2705 {user.name} verified.")
                        cur.execute("INSERT INTO verified_users (email, user_id) VALUES (%s, %s)", (email, user.id))
                        conn.commit()
                    else:
                        await message.channel.send("\u26a0\ufe0f Could not assign role. Please contact an admin.")
                else:
                    await message.channel.send("\u274c OTP expired. Please restart verification.")
            else:
                await message.channel.send("\u274c Invalid OTP.")
        else:
            await message.channel.send("\u26a0\ufe0f Please enter a valid email or OTP.")

bot.run(DISCORD_TOKEN)
