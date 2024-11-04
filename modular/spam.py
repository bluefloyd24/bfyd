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

    reply = m.reply_to_message

    # Mengedit pesan perintah asli menjadi "proses" dan kemudian menghapusnya
    try:
        msg = await m.edit(cgr("proses").format(em.proses))
        await msg.delete()  # Hapus pesan "proses" setelah diedit
    except Exception as error:
        return await m.reply(f"Error: {error}")

    berenti = True
    
    try:
        # Mengambil parameter jumlah pesan dan delay waktu dari perintah
        count_message = int(m.command[1])
        count_delay = int(m.command[2])
    except (IndexError, ValueError):
        return await m.reply(cgr("spm_2").format(em.gagal, m.command))  # Menampilkan pesan error jika perintah salah atau kurang lengkap

    await asyncio.sleep(count_delay)  # Delay pertama sebelum memulai loop pengiriman pesan

    # Proses pengiriman pesan berulang
    if reply:
        for i in range(count_message):
            if not berenti:
                break
            try:
                await reply.copy(m.chat.id)  # Menyalin pesan yang di-reply ke chat
                await asyncio.sleep(count_delay)  # Delay antar-pesan
            except Exception as e:
                await m.reply(f"Error: {e}")
                break
    else:
        if len(m.command) < 4:
            return await m.reply(cgr("spm_2").format(em.gagal, m.command))  # Menampilkan pesan error jika perintah kurang lengkap
        
        # Mengambil teks yang ingin dikirim dalam perulangan
        text_to_send = m.text.split(None, 3)[3]
        for i in range(count_message):
            if not berenti:
                break
            try:
                await c.send_message(m.chat.id, text_to_send)  # Mengirim pesan sebagai pesan baru
                await asyncio.sleep(count_delay)  # Delay antar-pesan
            except Exception as e:
                await m.reply(f"Error: {e}")
                break

    berenti = False
    await m.delete()  # Menghapus pesan perintah asli setelah proses selesai

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

    # Mengedit pesan perintah asli menjadi "proses"
    proses = await message.edit(cgr("proses").format(em.proses))

    # Menghapus pesan perintah setelah diubah menjadi "proses"
    await proses.delete()

    berenti = True

    try:
        _, count_str, delay_str, link = proses.text.split(maxsplit=3)
        count = int(count_str)
        delay = int(delay_str)
    except ValueError:
        await proses.edit(cgr("spm_5").format(em.gagal, message.command))
        await proses.delete()
        return

    # Mendapatkan chat_id dan message_id dari link
    chat_id, message_id = link.split("/")[-2:]

    try:
        chat_id = int(chat_id)
    except ValueError:
        pass

    message_id = int(message_id)

    # Loop pengiriman pesan dengan delay di awal loop
    for _ in range(count):
        try:
            if not berenti:
                break

            # Menunggu delay sebelum pengiriman pertama
            await asyncio.sleep(delay)

            # Mengambil pesan dari chat_id dan message_id lalu meneruskan ke chat saat ini
            await c.get_messages(chat_id, message_id)
            await c.forward_messages(proses.chat.id, chat_id, message_ids=message_id)

        except Exception as e:
            if (
                "CHAT_SEND_PHOTOS_FORBIDDEN" in str(e)
                or "CHAT_SEND_MEDIA_FORBIDDEN" in str(e)
                or "USER_RESTRICTED" in str(e)
            ):
                await proses.reply(cgr("spm_6").format(em.gagal))
                await proses.delete()
            else:
                await proses.reply(cgr("err").format(em.gagal, e))
                await proses.delete()
            break

    # Menghapus pesan proses dan mengatur ulang flag berenti
    berenti = False
    await proses.delete()
