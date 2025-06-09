# Telegram-bot-download

**Telegram-bot-download** is a simple Python Telegram bot that lets you download videos from **YouTube, TikTok, Instagram, and X (Twitter)** by just sending the video link to the bot. I made it quickly and simply for a friend, so it's straightforward and easy to use.

## Features

- Download videos from **YouTube, TikTok, Instagram, and X (Twitter)**.
- Choose to download X (Twitter) videos as **MP4 or GIF**.
- Automatic handling of cookies for authenticated downloads.
- Simple usage via Telegram chat commands.

## How to Use

### Requirements

- Python 3.x
- `yt-dlp` package
- A Telegram bot token create one with [@BotFather](https://t.me/BotFather)
- Cookies files for TikTok, Instagram, Youtube, and X placed inside the `cookies` folder

### Setup

1. Clone the repository or download the code:
```bash
git clone https://github.com/Dansvn/telegram-video-downloader.git
```
2. Navigate to the project directory:
```bash
cd telegram-video-downloader
```
3. Install the required Python packages:
```bash
pip install -r requirements.txt
```
4. Place your Telegram bot token in a token.json file:
```bash
{
  "token": "insert-your-token-here"
}

```
5. Add your cookies files inside the `cookies` folder:
- `cookies_instagram.txt` for Instagram
- `cookies_youtube.txt` for Youtube
- `cookies_tiktok.txt` for TikTok
-  `cookies_x.txt` for X (Twitter)

### Running the Bot

Run the bot with:
```bash
python index.py
```

### Using the Bot

- Start a chat with your bot on Telegram.
- Send `/start` to get instructions.
- Send any video link from YouTube, TikTok, Instagram, or X.
- For X (Twitter) links, you will be prompted to choose between downloading as a video or a GIF.
- The bot will download the video or GIF and send it back to you in the chat.
- If there is an error during the download, the bot will notify you.

---

## About

This bot is simple and I made it just for a friend. It’s a quick and practical tool to download videos from popular social platforms through Telegram.


---

## Contact

If you have any questions or need support, feel free to reach out!  
**My social links:** [ayo.so/dansvn](https://ayo.so/dansvn)

