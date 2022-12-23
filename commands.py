from configs import DISCORD_PREFIXS

from typing import Optional

from discord import Message, VoiceChannel

def text_retouch(string: str):
    removed = map(lambda sr: sr.strip(), string.split("\n"))
    joined = "\n".join(removed)
    return joined.strip()

class BaseCommand:
    @staticmethod
    async def help(raw_message: Message):
        raise NotImplementedError
    
    @staticmethod
    async def execute(raw_message: Message, args: Optional[tuple]=None):
        raise NotImplementedError

class Help(BaseCommand):
    @staticmethod
    async def help(raw_message: Message):
        _content = [
            f"指令有效開頭:`{'|'.join(DISCORD_PREFIXS)}`",
            f"",
            f"基礎設定 :",
            f"> `name <name>`   - 改變你的語音頻道名稱",
            f"> `limit <num>`   - 改變頻道限制人數",
            f"> `bitrate <num>` - 改變頻道的位元率",
            f"",
            f"隱私相關設定 :",
            f"> `hide`   - 將語音頻道隱藏，其他使用者無法看見該頻道",
            f"> `unhide` - 將語音頻道設為可見",
            f"> `lock`   - 將頻道上鎖，其他使用者無法加入",
            f"> `unlock` - 將頻道解鎖，其他使用者可以加入",
            f"",
            f"管理參與者 :",
            f"> `kick <tag>`  - 踢出語音頻道內的某個使用者",
            f"> `ban <tag>`   - 永久驅逐某個使用者",
            f"> `unban <tag>` - 解除驅逐某個使用者",
            f"",
            f"管理頻道 :",
            f"> `mute`              - 禁止所有人說話",
            f"> `unmute`            - 允許所有人說話",
            f"> `chmod <mod> <tag>` - 管理個別使用者之權限",
        ]
        _content = "\n".join(_content)
        await raw_message.reply(content=_content)
    
    @staticmethod
    async def execute(raw_message: Message, args: Optional[tuple]=None):
        if args == None:
            await Help.help(raw_message)