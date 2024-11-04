################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Misskaty
 
 MIKIR GOBLOK, TOLOL, IDIOT, NGENTOT, KONTOL, BAJINGAN
"""
################################################################


from os import execvp
from sys import executable
from sys import version as pyver

import wget
from pyrogram import __version__ as pyrover
from pyrogram.errors import ChannelInvalid, PeerIdInvalid
from pyrogram.types import ChatPrivileges
from pytgcalls import __version__ as pytgver
from team.nandev.class_log import LOGGER
from team.nandev.class_modules import CMD_HELP
from team.nandev.database import ndB

from config import log_channel, log_pic
from Mix import bot, nlx

chat_id = int(log_channel) if log_channel else ndB.get_key("TAG_LOG")


async def check_logger():
    # if not ndB.get_key("TAG_LOG") and log_channel is None:
    if not chat_id:
        LOGGER.info("Creating Grup Log...")
        nama = "botlogs.-𝐁𝘭𝘶𝘦𝘧𝘭𝘰𝘺𝘥 v2"
        des = "𝗝𝗮𝗻𝗴𝗮𝗻 leave grup!\n\nrenewal just chat @blque"
        log_pic = "https://telegra.ph/file/78fbd9d73e1f456857222.jpg"
        gc = await nlx.create_supergroup(nama, des)
        bhan = wget.download(f"{log_pic}")
        gmbr = {"video": bhan} if bhan.endswith(".mp4") else {"photo": bhan}
        kntl = gc.id
        await nlx.set_chat_photo(kntl, **gmbr)
        await nlx.promote_chat_member(
            kntl,
            bot.me.username,
            privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ),
        )
        ndB.set_key("TAG_LOG", int(kntl))
        await nlx.send_message(kntl, "berhasil membuat group logs. -blue")
        LOGGER.info("Group Logger Enable...")
        execvp(executable, [executable, "-m", "Mix"])
    else:
        return


async def getFinish():
    emut = await nlx.get_prefix(nlx.me.id)
    xx = " ".join(emut)
    try:
        await bot.send_message(
            int(chat_id),
            f"""
𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗶𝘀 𝗮𝗰𝘁𝗶𝘃𝗲 !
      𝗠𝗼𝗱𝘂𝗹𝗲: <b>{len(CMD_HELP)}</b>
      𝗣𝘆𝘁𝗵𝗼𝗻: <b>{pyver.split()[0]}</b>
      𝗣𝘆𝗿𝗼𝗴𝗿𝗮𝗺: <b>{pyrover}</b>
      𝗣𝘆𝘁𝗴𝗰𝗮𝗹𝗹𝘀: <b>{pytgver}</b>
      𝗣𝗿𝗲𝗳𝗶𝘅𝗲𝘀: <b>{xx}</b>
""",
        )
    except (ChannelInvalid, PeerIdInvalid):
        try:
            await nlx.promote_chat_member(
                int(chat_id),
                bot.me.username,
                privileges=ChatPrivileges(
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                ),
            )
            await bot.send_message(
                int(chat_id),
                f"""
𝗨𝘀𝗲𝗿𝗯𝗼𝘁 𝗶𝘀 𝗮𝗰𝘁𝗶𝘃𝗲 !
      𝗠𝗼𝗱𝘂𝗹𝗲: <b>{len(CMD_HELP)}</b>
      𝗣𝘆𝘁𝗵𝗼𝗻: <b>{pyver.split()[0]}</b>
      𝗣𝘆𝗿𝗼𝗴𝗿𝗮𝗺: <b>{pyrover}</b>
      𝗣𝘆𝘁𝗴𝗰𝗮𝗹𝗹𝘀: <b>{pytgver}</b>
      𝗣𝗿𝗲𝗳𝗶𝘅𝗲𝘀: <b>{xx}</b>
""",
            )
        except:
            ndB.del_key("TAG_LOG")
            execvp(executable, [executable, "-m", "Mix"])
