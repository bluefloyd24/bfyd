################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import os
import subprocess
import time
from datetime import timedelta
from time import time
from urllib.parse import urlparse

import requests
import wget
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.file_id import *
from pyrogram.raw.functions.messages import *
from pyrogram.types import *
from youtubesearchpython import VideosSearch

from Mix import Emojik, YoutubeDownload, cgr, get_cgr, ky, nlx, progress

__modles__ = "Download"
__help__ = get_cgr("help_download")


def get_video_dimensions(file_path):
    width, height = 0, 0
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=p=0:s=x",
        file_path,
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        dimensions = result.stdout.decode().split("x")
        if len(dimensions) == 2:
            width, height = map(int, dimensions)
    return width, height


def clear_directory(directory):
    command = ["rm", "-rf", directory]
    subprocess.run(command)


async def download_tiktok_video(c, chat_id, tiktok_link):
    try:
        output_filename = "media/downloaded_video.%(ext)s"

        command = ["yt-dlp", "-o", output_filename, tiktok_link]
        subprocess.check_call(command)

        width, height = get_video_dimensions("media/downloaded_video.mp4")

        with open("media/downloaded_video.mp4", "rb") as video_file:
            await c.send_video(
                chat_id=chat_id,
                video=video_file,
                width=width,
                height=height,
            )

        clear_directory("media")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        await c.send_message(
            chat_id=chat_id, text="Tautan rusak atau video gagal diunggah."
        )


@ky.ubot("dtik", sudo=False)
async def download_tiktok_command(c: nlx, m: Message):
    em = Emojik()
    em.initialize()
    tiktok_link = m.text.split(maxsplit=1)[1]
    pros = await m.edit(cgr("proses").format(em.proses))

    await download_tiktok_video(c, m.chat.id, tiktok_link)

    await pros.delete()


@ky.ubot("vtube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_video(
        m.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "VIDEO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@ky.ubot("stube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_audio(
        m.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "AUDIO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


def is_valid_twitter_url(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc.endswith("x.com") and "/status/" in parsed_url.path


def download_media_from_twitter(tweet_url):
    endpoint = "https://twitter-x-media-download.p.rapidapi.com/media"
    payload = {"url": tweet_url, "proxy": ""}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "twitter-x-media-download.p.rapidapi.com",
    }

    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if "tweetResult" in data:
            return data["tweetResult"]
        else:
            return None
    else:
        return None


async def download_and_send_file(nlx, chat_id, url, content_type):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            file_name = f"downloaded_{content_type}.{url.split('.')[-1]}"
            with open(file_name, "wb") as f:
                f.write(response.content)
            if content_type == "photo":
                await nlx.reply_photo(chat_id, file_name)
            elif content_type == "video":
                await nlx.reply_video(chat_id, file_name)
            os.remove(file_name)
    except Exception as e:
        await nlx.reply("Terjadi kesalahan saat mengunduh atau mengirim file.")


@ky.ubot("twit", sudo=True)
async def twit(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.edit(cgr("proses").format(em.proses))
    if len(m.command) < 2:
        await pros.edit(f"{em.gagal} <b>Silakan berikan tautan Twitter.</b>")
        return

    tweet_url = m.command[1]
    if not is_valid_twitter_url(tweet_url):
        await pros.edit(
            f"{em.gagal} <b>Tautan yang diberikan bukan tautan Twitter yang valid.</b>"
        )
        return
    media_info = download_media_from_twitter(tweet_url)

    if media_info:
        media_type = (
            media_info.get("result", {})
            .get("legacy", {})
            .get("entities", {})
            .get("media", [{}])[0]
            .get("type")
        )
        if media_type == "photo":
            media_url = (
                media_info.get("result", {})
                .get("legacy", {})
                .get("entities", {})
                .get("media", [{}])[0]
                .get("media_url_https")
            )
            if media_url:
                caption = f"{em.sukses} <b>Successfully Download Photo by : {c.me.mention}</b>"
                await c.send_photo(chat_id=m.chat.id, photo=media_url, caption=caption)
                await pros.delete()
        elif media_type == "video":
            video_info = (
                media_info.get("result", {})
                .get("legacy", {})
                .get("entities", {})
                .get("media", [{}])[0]
                .get("video_info", {})
            )
            if video_info:
                variants = video_info.get("variants", [])
                video_url = None
                for variant in variants:
                    content_type = variant.get("content_type", "")
                    if "video/mp4" in content_type:
                        video_url = variant.get("url", "")
                        break
                if video_url:
                    caption = f"{em.sukses} <b>Successfully Download Video by : {c.me.mention}</b>"
                    await c.send_video(
                        chat_id=m.chat.id, video=video_url, caption=caption
                    )
                    await pros.delete()
            else:
                await pros.edit(
                    f"{em.gagal} <b>Gagal mendapatkan URL video dari tautan Twitter.</b>"
                )
    else:
        await pros.edit(
            f"{em.gagal} <b>Gagal mendapatkan informasi media dari Twitter.</b>"
        )


@ky.ubot("insta", sudo=True)
async def insta_handler(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.edit(cgr("proses").format(em.proses))
    try:
        url = m.command[1]
        querystring = {"url": url}
        headers = {
            "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
            "X-RapidAPI-Host": "instagram-post-reels-stories-downloader.p.rapidapi.com",
        }
        response = requests.get(
            "https://instagram-post-reels-stories-downloader.p.rapidapi.com/instagram/",
            headers=headers,
            params=querystring,
        )
        data = response.json()
        if data["status"]:
            result = data["result"][0]
            media_url = result["url"]
            thumb_url = result["thumb"]
            await c.send_video(m.chat.id, video=media_url, thumb=thumb_url)
        else:
            await pros.edit(
                f"{em.gagal} <b>Gagal mengunduh media dari tautan yang diberikan.</b>"
            )
    except IndexError:
        await pros.edit(
            f"{em.gagal} <b>Format perintah salah.\nGunakan perintah `{m.text} [tautan_instagram]`</b>."
        )
