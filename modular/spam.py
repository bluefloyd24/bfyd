################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import asyncio

from pyrogram.errors import *

from Mix import *

dispam = []

berenti = False

__modles__ = "Spam"
__help__ = get_cgr("help_spam")


@ky.ubot("spam")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    global berenti
    reply = m.reply_to_message
    msg = await m.reply(cgr("proses").format(em.proses))
    berenti = True

    if reply:
        try:
            count_message = int(m.command[1])
            for i in range(count_message):
                if not berenti:
                    break
                await reply.copy(m.chat.id)
                msg.delete()
                await asyncio.sleep(0.1)
        except Exception as error:
            return await msg.edit(str(error))
    else:
        if len(m.command) < 2:
            return await msg.edit(cgr("spm_1").format(em.gagal, m.command))

        else:
            try:
                count_message = int(m.command[1])
                for i in range(count_message):
                    if not berenti:
                        break
                    await m.reply(
                        m.text.split(None, 2)[2],
                    )
                    await asyncio.sleep(0.1)
            except Exception as error:
                return await msg.edit(str(error))
    berenti = False

    await msg.delete()
    await m.delete()


@ky.ubot("dspam")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    global berenti

    # Check if the chat is in the blacklist
    if m.chat.id in BLACKLIST_CHAT:
        return await m.reply("Not work on this group!")  # You can replace with your own blacklist message

    reply = await m.reply_to_message
    input_str = m.text.split(maxsplit=2)  # Get input after the command
    try:
        # Parse the count and delay from the command input
        count_message = int(input_str[1])
        count_delay = float(input_str[2])  # Allow for decimal values for delay
        message_text = input_str[3] if len(input_str) > 3 else ""  # Message text
    except (ValueError, IndexError):
        return await m.reply("Usage: .dspam <count> <delay> <message>\nExample: .dspam 5 2 Hello")

    await m.delete()  # Delete the command message to keep the chat clean
    berenti = True  # Set to True to allow the process to continue

    if reply:  # If replying to a message
        for _ in range(count_message):
            if not berenti:
                break
            await reply.copy(m.chat.id)  # Copy the replied message to the chat
            await asyncio.sleep(count_delay)  # Wait for the specified delay
    else:  # If no reply, send the specified message text
        for _ in range(count_message):
            if not berenti:
                break
            await m.reply(message_text)  # Send the provided message text
            await asyncio.sleep(count_delay)  # Wait for the specified delay

    berenti = False  # Reset the stopping variable

    # Optionally inform the user when done
    await m.reply("Done sending messages.")


    berenti = False

    await msg.delete()
    await m.delete()


@ky.ubot("cspam")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    global berenti
    if not berenti:
        return await m.reply(cgr("spm_3").format(em.gagal))
    berenti = False
    await m.reply(cgr("spm_4").format(em.sukses))
    return


@ky.ubot("dspamfw")
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    global berenti
    message.reply_to_message
    proses = await message.reply(cgr("proses").format(em.proses))
    berenti = True

    try:
        _, count_str, delay_str, link = message.text.split(maxsplit=3)
        count = int(count_str)
        delay = int(delay_str)
    except ValueError:
        await proses.reply(cgr("spm_5").format(em.gagal, message.command))
        await proses.delete()
        return

    chat_id, message_id = link.split("/")[-2:]

    try:
        chat_id = int(chat_id)
    except ValueError:
        pass

    message_id = int(message_id)

    for _ in range(count):
        try:
            if not berenti:
                break
            await c.get_messages(chat_id, message_id)
            await c.forward_messages(message.chat.id, chat_id, message_ids=message_id)
            await proses.delete()
            await message.delete()
            await asyncio.sleep(delay)
        except Exception as e:
            if (
                "CHAT_SEND_PHOTOS_FORBIDDEN" in str(e)
                or "CHAT_SEND_MEDIA_FORBIDDEN" in str(e)
                or "USER_RESTRICTED" in str(e)
            ):
                await message.reply(cgr("spm_6").format(em.gagal))
                await proses.delete()
            else:
                await proses.reply(cgr("err").format(em.gagal, e))
                await proses.delete()
            break
    berenti = False
    await message.delete()
    await proses.delete()
