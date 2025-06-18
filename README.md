# Algopath Discord Access & Doubt Tracker Bot

A secure and structured Discord bot for the Algopath community that handles **email-based user verification** and **academic doubt tracking** — designed for educational communities like **Algopath**.

---

## Overview

This bot is designed to provide a **secure authentication flow** for new Discord users:

1️⃣ User joins the server via an invite link.  
2️⃣ User sends their registered email.  
3️⃣ Bot sends a **One-Time Password (OTP)** to that email.  
4️⃣ User enters the OTP in the Discord server.  
5️⃣ Bot verifies the OTP, and if correct, assigns the `Verified` role, granting access to main channels.

After joining, users can post academic doubts in a designated #doubts channel, and mark them as resolved with a simple reply. This keeps discussions organized, searchable, and accountable.

---

## Features

### 1. Secure Email-Based Verification
- Only **pre-approved email IDs** can start the verification process.
- An **OTP is emailed** to the user, valid for 10 minutes.
- **Each email can be used only once**, ensuring one account per user.
- After verification, the bot:
  - Assigns a `Verified` role
  - Tracks the user's **Discord ID** for long-term identity persistence

### 2. Smart Doubt Tracking
- Users can post doubts in a `#doubts` channel.
- Each message is logged in a PostgreSQL database.
- Users **reply to their own doubt** with `"resolved"` to mark it complete.
- The bot updates the status in the DB and sends a confirmation message.

---

## Technologies Used

- **Python 3.9+**  
- **discord.py** – for Discord bot integration  
- **PostgreSQL** – for storing user data and OTPs  
- **psycopg2** – Python driver for PostgreSQL  
- **dotenv** – for managing environment variables securely
- SMTP(Gmail) for sending OTPs  

---

## Database Schema (PostgreSQL)

- **emails** – Stores pre-approved email addresses.
- **otps** – Tracks generated OTPs with timestamps.
- **verified_users** – Stores verified email and Discord user ID.
- **doubts** – Logs all doubts, authors, message IDs, and resolution status.

---

## How to Use

- User joins the server and receives a DM asking for their registered email.
- If the email exists in the emails table and hasn’t been used:
  - An OTP is sent to their email.
  - User enters OTP in DM.
- If OTP is valid and timely:
  - Bot assigns them a “Verified” role.
  - They gain access to the server.
- To ask a doubt:
  - Post directly in #doubts.
  - Once resolved, reply to your original message with resolved.

---
