################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################


from Mix import *
from Mix.core.http import get

__modles__ = "Repository"
__help__ = get_cgr("help_repo")


@ky.ubot("repo|repository")
async def repo(c, m):
    link = await get("https://api.github.com/bluefloyd24/bfyd")
    orgnya = "".join(
        f"**{count}.** [{org['login']}]({org['html_url']})\n"
        for count, org in enumerate(link, start=1)
    )
    msg = f"""<b>[Github](https://github.com/bluefloyd24/bfyd) | [Group](t.me/proofniyeee)
```--------------
| devs?nah!! |
--------------```
{orgnya}</b>"""
    await c.send_message(
        m.chat.id, msg, reply_to_message_id=ReplyCheck(m), disable_web_page_preview=True
    )
