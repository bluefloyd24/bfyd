################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from telegraph import Telegraph, upload_file
from telegraph.exceptions import TelegraphException

from Mix import *

__modles__ = "Telegraph"
__help__ = get_cgr("help_graph")

@ky.ubot("tg")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    xx = await m.reply(cgr("proses").format(em.proses))
    if not m.reply_to_message:
        return await xx.edit(cgr("grp_1").format(em.gagal))

    telegraph = Telegraph()
    if m.reply_to_message.media:
        m_d = await m.reply_to_message.download()
        if not m_d:
            return await xx.edit("Failed to download the media.")

        try:
            media_url = upload_file(m_d)
            dnbg = cgr("grp_3").format(em.sukses, media_url[0], disable_web_page_preview=True)
            await xx.edit(dnbg, disable_web_page_preview=True)
        except TelegraphException as r:
            return await xx.edit(cgr("err").format(em.gagal, str(r)))
    elif m.reply_to_message.text:
        page_title = f"{c.me.first_name} {c.me.last_name or ''}"
        page_text = m.reply_to_message.text.replace("\n", "<br>")
        
        try:
            response = telegraph.create_page(page_title, html_content=page_text)
            ybg = cgr("grp_5").format(em.sukses, response["path"], disable_web_page_preview=True)
            await xx.edit(ybg, disable_web_page_preview=True)
        except TelegraphException as r:
            return await xx.edit(cgr("err").format(em.gagal, str(r)))
