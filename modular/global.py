################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

__modles__ = "Global"
__help__ = """
 Help Command Global

• Perintah : <code>{0}gban</code> [user_id/username/bales pesan]
• Penjelasan : Untuk melakukan global banned.

• Perintah : <code>{0}ungban</code> [user_id/username/bales pesan]
• Penjelasan : Untuk melakukan global ubanned.

• Perintah : <code>{0}listgban</code> [user_id/username/bales pesan]
• Penjelasan : Untuk melihat daftar pengguna gban.

• Perintah : <code>{0}gmute</code> [user_id/username/bales pesan]
• Penjelasan : Untuk melakukan global mute.

• Perintah : <code>{0}ungmute</code> [user_id/username/bales pesan]
• Penjelasan : Untuk melakukan global unmute.

• Perintah : <code>{0}listgmute</code> [user_id/username/bales pesan]
• Penjelasan : Untuk melihat daftar pengguna gmute.
"""


import asyncio
from pyrogram import *
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *
from Mix import *


@ky.ubot("gban", sudo=True)
@ky.devs("cgban")
async def _(c: user, m):
    
    
    nyet, alasan = await c.extract_user_and_reason(m)
    xx = await m.reply(f"{proses} Processing...")
    try:
        org = await c.get_users(nyet)
    except PeerIdInvalid:
        await xx.edit(f"{gagal} Pengguna tidak ditemukan.")
        return
    if not org:
        await xx.edit(f"{gagal} Pengguna tidak ditemukan.")
        return
    if org.id in DEVS:
        await xx.edit(f"{gagal} Dia adalah Developer Mix-Userbot.")
        return
    bs = 0
    gg = 0
    chats = await c.get_user_dialog("all")
    gban_users = udB.get_list_from_var(c.me.id, "GBANNED", "USER")
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = (
            m.reply_to_message.sender_chat.title
            if m.reply_to_message
            else "Anon")
    for chat in chats:
        if org.id in gban_users:
            await xx.edit(f"{gagal} Pengguna sudah digban.")
            return
        try:
            await c.ban_chat_member(chat, org.id)
            bs += 1
            await asyncio.sleep(0.1)
        
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
            await c.ban_chat_member(chat, org.id)
            bs += 1
        except BaseException:
            gg += 1
            await asyncio.sleep(0.1)
    udB.add_to_var(c.me.id, "GBANNED", org.id, "USER")
    mmg = f"{warn} <b>Warning Global Banned\n\n{sukses} Berhasil: `{bs}` Chat\n{gagal} Gagal: `{gg}` Chat\n{profil} User: `{mention}`</b>\n"
    if alasan:
        mmg += f"{block} **Alasan: `{alasan}`**"
    await m.reply(mmg)
    await xx.delete()

@ky.ubot("ungban", sudo=True)
@ky.devs("cungban")
async def _(c: user, m):
    
    
    nyet = await c.extract_user(m)
    xx = await m.reply(f"{proses} Processing...")
    org = await c.get_users(nyet)
    if not org:
        await xx.edit(f"{gagal} Pengguna tidak ditemukan.")
        return
    bs = 0
    gg = 0
    chats = await c.get_user_dialog("all")
    gban_users = udB.get_list_from_var(c.me.id, "GBANNED", "USER")
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = (
            m.reply_to_message.sender_chat.title
            if m.reply_to_message
            else "Anon")
    for chat in chats:
        if org.id not in gban_users:
            await xx.edit(f"{gagal} Pengguna belum digban.")
            return
        try:
            await c.unban_chat_member(chat, org.id)
            bs += 1
            await asyncio.sleep(0.1)
        except BaseException:
            gg += 1
            await asyncio.sleep(0.1)
    udB.remove_from_var(c.me.id, "GBANNED", org.id, "USER")
    mmg = f"{warn} <b>Warning Global Unbanned\n\n{sukses} Berhasil: `{bs}` Chat\n{gagal} Gagal: `{gg}` Chat\n{profil} User: `{mention}`</b>\n"
    await m.reply(mmg)
    await xx.delete()

@ky.ubot("gmute", sudo=True)
@ky.devs("cgmute")
async def _(c: user, m):
    
    
    nyet, alasan = await c.extract_user_and_reason(m)
    xx = await m.reply(f"{proses} Processing...")
    org = await c.get_users(nyet)
    if not org:
        await xx.edit(f"{gagal} Pengguna tidak ditemukan.")
        return
    if org.id in DEVS:
        await xx.edit(f"{gagal} Dia adalah Developer Mix-Userbot.")
        return
    bs = 0
    gg = 0
    chats = await c.get_user_dialog("group")
    gmute_users = udB.get_list_from_var(c.me.id, "GMUTE", "USER")
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = (
            m.reply_to_message.sender_chat.title
            if m.reply_to_message
            else "Anon")
    for chat in chats:
        if org.id in gmute_users:
            await xx.edit(f"{gagal} Pengguna sudah digmute.")
            return
        try:
            await c.restrict_chat_member(chat, org.id, ChatPermissions())
            bs += 1
            await asyncio.sleep(0.1)
        except BaseException:
            gg += 1
            await asyncio.sleep(0.1)
    udB.add_to_var(c.me.id, "GMUTE", org.id, "USER")
    mmg = f"{warn} <b>Warning Global Gmute\n\n{sukses} Berhasil: `{bs}` Chat\n{gagal} Gagal: `{gg}` Chat\n{profil} User: `{mention}`</b>\n"
    if alasan:
        mmg += f"{block} **Alasan: `{alasan}`**"
    await m.reply(mmg)
    await xx.delete()
    

@ky.ubot("ungmute", sudo=True)
@ky.devs("cungmute")
async def _(c: user, m):
    
    
    nyet = await c.extract_user(m)
    xx = await m.reply(f"{proses} Processing...")
    org = await c.get_users(nyet)
    if not org:
        await xx.edit(f"{gagal} Pengguna tidak ditemukan.")
        return
    if org.id in DEVS:
        await xx.edit(f"{gagal} Dia adalah Developer Mix-Userbot.")
        return
    bs = 0
    gg = 0
    chats = await c.get_user_dialog("group")
    gmute_users = udB.get_list_from_var(c.me.id, "GMUTE", "USER")
    try:
        mention = (await c.get_users(nyet)).mention
    except IndexError:
        mention = (
            m.reply_to_message.sender_chat.title
            if m.reply_to_message
            else "Anon")
    for chat in chats:
        if org.id not in gmute_users:
            await xx.edit(f"{gagal} Pengguna belum pernah digmute.")
            return
        try:
            await c.unban_member(chat, org.id, ChatPermissions())
            bs += 1
            await asyncio.sleep(0.1)
        except BaseException:
            gg += 1
            await asyncio.sleep(0.1)
    udB.remove_from_var(c.me.id, "GMUTE", org.id, "USER")
    mmg = f"{warn} <b>Warning Global Ungmute\n\n{sukses} Berhasil: `{bs}` Chat\n{gagal} Gagal: `{gg}` Chat\n{profil} User: `{mention}`</b>\n"
    await m.reply(mmg)
    await xx.delete()
    
    
@ky.ubot("gbanlist|listgban", sudo=True)
async def _(c: user, m):
    
    
    gban_list = []
    msg = await m.reply(f"{proses} <b>Processing...</b>")
    gbanu = udB.get_list_from_var(c.me.id, "GBANNED", "USER")
    if not gbanu:
        return await msg.edit(f"{gagal} <b>Tidak ada pengguna ditemukan.</b>")
    for x in gbanu:
        try:
            org = await c.get_users(int(x))
            gban_list.append(
                f"{profil} • [{user.first_name} {user.last_name or ''}](tg://user?id={org.id}) | <code>{org.id}</code>")
        except:
            continue
    if gban_list:
       stak = (
            f"{profil} <b>Daftar Pengguna:</b>\n"
            + "\n".join(gban_list)
            + f"\n{sukses} <code>{len(gban_list)}</code>")
       return await msg.edit(stak)
    else:
        return await msg.edit(f"{gagal} <b>Eror</b>")
        
        

@ky.ubot("gmutelist|listgmute", sudo=True)
async def _(c: user, m):
    
    
    gmute_list = []
    msg = await m.reply(f"{proses} <b>Processing...</b>")
    gmute = udB.get_list_from_var(c.me.id, "GMUTE", "USER")
    if not gmute:
        return await msg.edit(f"{gagal} <b>Tidak ada pengguna ditemukan.</b>")
    for x in gmute:
        try:
            org = await c.get_users(int(x))
            gmute_list.append(
                f"{profil} • [{user.first_name} {user.last_name or ''}](tg://user?id={org.id}) | <code>{org.id}</code>")
        except:
            continue
    if gmute_list:
       stak = (
            f"{profil} <b>Daftar Pengguna:</b>\n"
            + "\n".join(gmute_list)
            + f"\n{sukses} <code>{len(gmute_list)}</code>")
       return await msg.edit(stak)
    else:
        return await msg.edit(f"{gagal} <b>Eror</b>")