from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import logging
import yt_dlp
import os
import json

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.json")
try:
    with open(TOKEN_PATH, "r") as f:
        TOKEN = json.load(f).get("token")
    if not TOKEN:
        raise ValueError("Token not found in token.json")
except Exception as e:
    logger.error(f"Error loading token: {e}")
    exit(1)

COOKIE_DIR = os.path.join(BASE_DIR, "cookies")
COOKIES_TIKTOK = os.path.join(COOKIE_DIR, 'cookies_tiktok.txt')
COOKIES_INSTAGRAM = os.path.join(COOKIE_DIR, 'cookies_instagram.txt')
COOKIES_X = os.path.join(COOKIE_DIR, 'cookies_x.txt')
COOKIES_YT = os.path.join(COOKIE_DIR, 'cookies.yt')

DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

CHOICE_X = range(1)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send the video link (YouTube, TikTok, Instagram or X).')

async def handle_others(update: Update, context: CallbackContext, url: str):
    user = update.effective_user
    if 'youtube.com' in url or 'youtu.be' in url:
        await update.message.reply_text('Please wait...')
        logger.info(f"User {user.id} (@{user.username}) started YouTube download: {url}")
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'cookiefile': COOKIES_YT,
            'playlist_items': '1',
        }
    elif 'tiktok.com' in url:
        await update.message.reply_text('Please wait...')
        logger.info(f"User {user.id} (@{user.username}) started TikTok download: {url}")
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'cookiefile': COOKIES_TIKTOK,
        }
    elif 'instagram.com' in url:
        await update.message.reply_text('Please wait...')
        logger.info(f"User {user.id} (@{user.username}) started Instagram download: {url}")
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            'cookiefile': COOKIES_INSTAGRAM,
        }
    else:
        logger.warning(f"User {user.id} (@{user.username}) sent unsupported link: {url}")
        await update.message.reply_text('Invalid or unsupported link, or you sent text instead of a link >:(')
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if 'entries' in info_dict and len(info_dict['entries']) > 0:
                video_info = info_dict['entries'][0]
                if 'requested_downloads' in video_info and video_info['requested_downloads']:
                    filename = video_info['requested_downloads'][0]['filepath']
                else:
                    filename = ydl.prepare_filename(video_info)
            else:
                if 'requested_downloads' in info_dict and info_dict['requested_downloads']:
                    filename = info_dict['requested_downloads'][0]['filepath']
                else:
                    filename = ydl.prepare_filename(info_dict)
            logger.info(f"User {user.id} (@{user.username}) successfully downloaded: {filename}")

        with open(filename, 'rb') as f:
            await update.message.reply_video(f)

        os.remove(filename)
        logger.info(f"User {user.id} (@{user.username}) file removed: {filename}")
    except Exception as e:
        logger.error(f"User {user.id} (@{user.username}) download error: {str(e)}")
        await update.message.reply_text('Error downloading the video, contact me if it keeps failing')

async def download(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    url = update.message.text
    context.user_data['url'] = url
    logger.info(f"User {user.id} (@{user.username}) sent URL: {url}")
    if 'x.com' in url or 'twitter.com' in url:
        await update.message.reply_text("Type:\n1 to download as video\n2 to download as GIF")
        return CHOICE_X
    await handle_others(update, context, url)
    return ConversationHandler.END

async def choose_x(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    choice = update.message.text.strip()
    url = context.user_data['url']
    if choice == '1':
        ext = 'mp4'
    elif choice == '2':
        ext = 'gif'
    else:
        await update.message.reply_text("Invalid option. Please type 1 or 2.")
        return CHOICE_X
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': os.path.join(DOWNLOADS_DIR, f'%(title)s.{ext}'),
        'cookiefile': COOKIES_X,
    }
    await update.message.reply_text('Please wait...')
    logger.info(f"User {user.id} (@{user.username}) started X download as {ext.upper()}: {url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            if 'entries' in info_dict and len(info_dict['entries']) > 0:
                video_info = info_dict['entries'][0]
                if 'requested_downloads' in video_info and video_info['requested_downloads']:
                    filename = video_info['requested_downloads'][0]['filepath']
                else:
                    filename = ydl.prepare_filename(video_info)
            else:
                if 'requested_downloads' in info_dict and info_dict['requested_downloads']:
                    filename = info_dict['requested_downloads'][0]['filepath']
                else:
                    filename = ydl.prepare_filename(info_dict)
            logger.info(f"User {user.id} (@{user.username}) successfully downloaded X file: {filename}")

        with open(filename, 'rb') as f:
            if ext == 'gif':
                await update.message.reply_document(f)
            else:
                await update.message.reply_video(f)

        os.remove(filename)
        logger.info(f"User {user.id} (@{user.username}) X file removed: {filename}")
    except Exception as e:
        logger.error(f"User {user.id} (@{user.username}) X download error: {str(e)}")
        await update.message.reply_text('Error downloading from X. Contact me if it keeps failing.')

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    user = update.effective_user
    logger.info(f"User {user.id} (@{user.username}) cancelled the operation.")
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

def main():
    logger.info("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, download)],
        states={CHOICE_X: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_x)]},
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(CommandHandler('start', start))
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
