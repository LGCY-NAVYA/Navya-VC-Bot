from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from plugins.vc.handlers import skip_current_song, skip_item
from plugins.vc.queues import QUEUE, clear_queue

@Client.on_message(contact_filter & filters.command(['skip', 'next', 'n', '/skip', '/next'], prefixes=f"{HNDLR}"))
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**🙄𝑻𝒉𝒆𝒓𝒆❜𝒔 𝒏𝒐𝒕𝒉𝒊𝒏𝒈 𝒊𝒏 𝒕𝒉𝒆 𝒒𝒖𝒆𝒖𝒆 𝒕𝒐 𝒔𝒌𝒊𝒑!**")
        elif op == 1:
            await m.reply("**😩𝑬𝒎𝒑𝒕𝒚 𝑸𝒖𝒆𝒖𝒆, 𝑳𝒆𝒂𝒗𝒊𝒏𝒈 𝑽𝒐𝒊𝒄𝒆 𝑪𝒉𝒂𝒕**")
        else:
            await m.reply(
                f"**⏭ Skipped** \n**🎧 Now playing** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ 𝑹𝒆𝒎𝒐𝒗𝒆𝒅 𝒕𝒉𝒆 𝒇𝒐𝒍𝒍𝒐𝒘𝒊𝒏𝒈 𝒔𝒐𝒏𝒈𝒔 𝒇𝒓𝒐𝒎 𝒕𝒉𝒆 𝑸𝒖𝒆𝒖𝒆: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)        
      

@Client.on_message(contact_filter & filters.command(['end', 'stop', '/end', '/stop', 'x'], prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**😐End**")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**🤨𝑵𝒐𝒕𝒉𝒊𝒏𝒈 𝒊𝒔 𝒑𝒍𝒂𝒚𝒊𝒏𝒈 !**")

   
@Client.on_message(contact_filter & filters.command(['pause', '/pause', 'wait', 'ruko'], prefixes=f"{HNDLR}"))
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**⏸ Paused.**\n\n• To resume playback, use the command "
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**🤨Nothing is playing!**")
      

@Client.on_message(contact_filter & filters.command(['resume', 'r', '/resume'], prefixes=f"{HNDLR}"))
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**▶ Resumed**\n\n• To pause playback, use the command**"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**𝑵𝒐𝒕𝒉𝒊𝒏𝒈 𝒊𝒔 𝒄𝒖𝒓𝒓𝒆𝒏𝒕𝒍𝒚 𝒑𝒂𝒖𝒔𝒆𝒅❗**")
