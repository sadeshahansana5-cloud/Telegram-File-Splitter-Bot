<div align="center">

# 📁 Telegram File Splitter Bot

<img src="https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif" width="200" alt="Bot Animation">

### ✂️ Split Large Files into Telegram-Friendly Parts

[![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=36BCF7&center=true&vCenter=true&width=500&lines=Split+files+up+to+4GB;500MB+or+1GB+parts;Auto-upload+to+Telegram;Fast+%26+Reliable" alt="Typing Animation">
</p>

</div>

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📦 **Split Large Files** | Split files up to **4GB** into manageable parts |
| ⚡ **Two Size Options** | Choose between **500MB** or **1GB** per part |
| 🚀 **Live Progress** | Real-time progress bar with speed & ETA |
| 🐳 **Docker Ready** | Run anywhere with Docker containerization |
| ☁️ **GitHub Actions** | Deploy on GitHub Actions with one click |
| 🔄 **Auto Cleanup** | Temporary files deleted automatically |
| 📱 **Telegram Native** | Works seamlessly within Telegram |

---

## 🚀 Quick Start

### Option 1: Run on GitHub Actions (Free)

<p align="center">
  <img src="https://media.giphy.com/media/3oKIPEqDGUULpEU0aQ/giphy.gif" width="400" alt="GitHub Actions">
</p>

#### Step 1: Fork this Repository

Click the **Fork** button at the top right of this page.

#### Step 2: Add Your Telegram Credentials

Go to **Settings > Secrets and variables > Actions > New repository secret** and add these 3 secrets:

| Secret Name | Value | How to Get |
|-------------|-------|------------|
| `API_ID` | Your Telegram API ID | [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Your Telegram API Hash | [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Your Bot Token | [@BotFather](https://t.me/BotFather) |

<p align="center">
  <img src="https://docs.github.com/assets/cb-11477/images/help/repository/actions-secrets-tab.png" width="600" alt="Secrets Setup">
</p>

#### Step 3: Create Workflow File

Create `.github/workflows/run-bot.yml` and paste this code:

```yaml
name: Run Telegram Splitter Bot

on:
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout Repository
        uses: actions/checkout@v4

      - name: 🐳 Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: 🔧 Build Docker Image
        run: |
          docker build -t telegram-splitter-bot .

      - name: 🚀 Run Bot Container
        run: |
          docker run -d \
            --name splitter-bot \
            -p 7860:7860 \
            telegram-splitter-bot

      - name: ⏳ Wait & Check Logs
        run: |
          sleep 10
          echo "=== BOT LOGS ==="
          docker logs splitter-bot
          echo "================"
          echo "Bot is running... Keeping workflow alive for 6 hours"
          sleep 21600

```

#### Step 4: Run the Workflow

1. Go to the **Actions** tab
2. Click **"Run Telegram Splitter Bot"**
3. Click **"Run workflow"** button
4. Your bot is now live! 🎉

<p align="center">
  <img src="https://media.giphy.com/media/3oKIPnAiaMCws8n196/giphy.gif" width="300" alt="Success">
</p>

---

### Option 2: Run with Docker (Local/VPS)

#### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/telegram-splitter-bot.git
cd telegram-splitter-bot
```

#### Step 2: Set Environment Variables

```bash
export API_ID="your_api_id"
export API_HASH="your_api_hash"
export BOT_TOKEN="your_bot_token"
```

#### Step 3: Build and Run

```bash
docker build -t telegram-splitter-bot .

docker run -d \\
  -e API_ID="$API_ID" \\
  -e API_HASH="$API_HASH" \\
  -e BOT_TOKEN="$BOT_TOKEN" \\
  -p 7860:7860 \\
  --name splitter-bot \\
  telegram-splitter-bot
```

#### Step 4: Check Logs

```bash
docker logs -f splitter-bot
```

---

## 📸 How to Use

### 1. Start the Bot

Send `/start` to your bot on Telegram.

<p align="center">
  <img src="https://i.imgur.com/placeholder1.png" width="400" alt="Start Command">
</p>

### 2. Send Your File

Send any file (up to 4GB) to the bot.

<p align="center">
  <img src="https://i.imgur.com/placeholder2.png" width="400" alt="Send File">
</p>

### 3. Choose Split Size

Click either **500MB Parts** or **1GB Parts** button.

<p align="center">
  <img src="https://i.imgur.com/placeholder3.png" width="400" alt="Choose Size">
</p>

### 4. Wait for Processing

Watch the live progress with speed and ETA.

<p align="center">
  <img src="https://i.imgur.com/placeholder4.png" width="400" alt="Progress">
</p>

### 5. Download Parts

Receive all parts and extract with **7-Zip** or **WinRAR**.

<p align="center">
  <img src="https://i.imgur.com/placeholder5.png" width="400" alt="Download Parts">
</p>

---

## 🏗️ Project Structure

```
telegram-splitter-bot/
├── .github/
│   └── workflows/
│       └── run-bot.yml      # GitHub Actions workflow
├── bot.py                   # Main bot code
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pyrogram-FF6F00?style=for-the-badge&logo=telegram&logoColor=white" alt="Pyrogram">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/7--Zip-000000?style=for-the-badge&logo=7zip&logoColor=white" alt="7-Zip">
</p>

---

## ⚠️ Important Notes

| Note | Description |
|------|-------------|
| ⏱️ **GitHub Actions Limit** | Free tier runs max **6 hours** per workflow |
| 🔒 **Security** | Never commit API keys to public repos |
| 💾 **Storage** | GitHub Actions has limited disk space |
| 🔄 **Restart** | Workflow stops after 6h, click "Run workflow" again |

---

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `API_ID` | Yes | Telegram API ID from my.telegram.org |
| `API_HASH` | Yes | Telegram API Hash from my.telegram.org |
| `BOT_TOKEN` | Yes | Bot token from @BotFather |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

<p align="center">
  <img src="https://media.giphy.com/media/l3vR85PnGsBwu1PFK/giphy.gif" width="200" alt="Contributing">
</p>

---

## 📜 License

This project is licensed under the **MIT License**.

<p align="center">
  <img src="https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif" width="150" alt="License">
</p>

---

<div align="center">

### Made with ❤️ for Telegram Users

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=2000&pause=500&color=F75C7E&center=true&vCenter=true&width=400&lines=Happy+Splitting!;Enjoy+the+Bot!;Share+with+Friends!" alt="Closing Animation">
</p>

**⭐ Star this repo if you found it helpful!**

</div>
