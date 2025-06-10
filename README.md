# Algopath Discord Auth Bot

A secure Discord bot for the Algopath community that verifies users via email and OTP, and assigns them access roles.

---

## 📚 Overview

This bot is designed to provide a **secure authentication flow** for new Discord users:

1️⃣ User joins the server via an invite link.  
2️⃣ User sends their registered email.  
3️⃣ Bot sends a **One-Time Password (OTP)** to that email.  
4️⃣ User enters the OTP in the Discord server.  
5️⃣ Bot verifies the OTP, and if correct, assigns the `Verified` role, granting access to main channels.

The project uses **Python**, **discord.py**, and a **PostgreSQL database** to manage emails and OTPs.

---

## 🏗️ Features

- **Secure email verification** – ensures only legitimate users join.
- **OTP-based access** – adds an extra layer of security.
- **Role-based permissions** – only verified users can see main channels.
- **Database-backed** – uses PostgreSQL to store and validate data.
- **Fully customizable** – easy to adapt for your own Discord communities.

---

## ⚙️ Technologies Used

- **Python 3.9+**  
- **discord.py** – for Discord bot integration  
- **PostgreSQL** – for storing user data and OTPs  
- **psycopg2** – Python driver for PostgreSQL  
- **dotenv** – for managing environment variables securely  

---

## 🗂️ Project Structure

