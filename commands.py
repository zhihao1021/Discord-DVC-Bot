from configs import DISCORD_PREFIXS, DISCORD_LOGGER as LOG
import db_operation as dbo

from typing import Optional

from discord import Member, Message, VoiceChannel

def _is_admin(table_name: str, channel: VoiceChannel, user: Member) -> bool:
    # 取得管理員清單
    admin_list = dbo.get_admin(table_name, channel.id)
    # 檢查是否為管理員
    if user.id not in admin_list:
        # 如果不是管理員
        return False
    # 如果是管理員
    return True

class BaseCommand:
    @staticmethod
    async def help(raw_message: Message):
        raise NotImplementedError
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None):
        raise NotImplementedError

class Help(BaseCommand):
    @staticmethod
    async def help(raw_message: Message):
        _content = [
            f"指令有效開頭:`{'|'.join(DISCORD_PREFIXS)}`",
            f"可使用`help <command>`獲得詳細說明",
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
    async def execute(tabel_nam: str, raw_message: Message, args: Optional[tuple]=None):
        if args == None or len(args) < 1:
            await Help.help(raw_message)
        elif args[0] == "name":
            await Name.help(raw_message)
        elif args[0] == "limit":
            await Limit.help(raw_message)

class Name(BaseCommand):
    @staticmethod
    async def help(raw_message: Message):
        _e_prefix = DISCORD_PREFIXS[0]
        _content = [
            f"指令有效開頭:`{'|'.join(DISCORD_PREFIXS)}`",
            f"",
            f"指令 - `name <name>`",
            f"說明 : 將頻道名稱更改為`<name>`。",
            f"",
            f"參數說明 :",
            f"> `<name>` - 字串，新的頻道名稱。",
            f"",
            f"範例 :",
            f"> `{_e_prefix}name New_Channel_Name`",
            f"> `{_e_prefix}name new name`",
        ]
        _content = "\n".join(_content)
        await raw_message.reply(content=_content)
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None):
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            await raw_message.reply("你不是本頻道的管理員，無法使用該命令。")
            return

        # 檢查是否有參數傳入
        if args == None or len(args) < 1:
            await raw_message.reply("格式錯誤，請使用`help name`取得詳細說明。")
            return

        # 執行指令
        origin_name = channel.name
        new_name = " ".join(args)
        await channel.edit(name=new_name)
        await raw_message.reply(f"修改成功，已將頻道名稱由`{origin_name}`改為`{channel.name}`")
        LOG.info(f"Edit channel<{channel.guild.id}/{channel.id}> name from `{origin_name}` to `{channel.name}`")

class Limit(BaseCommand):
    @staticmethod
    async def help(raw_message: Message):
        _e_prefix = DISCORD_PREFIXS[0]
        _content = [
            f"指令有效開頭:`{'|'.join(DISCORD_PREFIXS)}`",
            f"",
            f"指令 - `limit <num>`",
            f"說明 : 將頻道人數上限更改為<num>人",
            f"",
            f"參數說明 :",
            f"> `<num>` - 整數或運算式，人數上限。",
            f"",
            f"範例 :",
            f"> `{_e_prefix}limit 10`",
            f"> `{_e_prefix}limit (7+8*6)/5-1`",
        ]
        _content = "\n".join(_content)
        await raw_message.reply(content=_content)
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None):
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            await raw_message.reply("你不是本頻道的管理員，無法使用該命令。")
            return
        
        # 檢查是否有參數傳入
        if args == None or len(args) < 1:
            await raw_message.reply("格式錯誤，請使用`help limit`取得詳細說明。")
            return
        else:
            # 如果有，則檢查是否可以轉為有效參數
            # 檢查是否可轉型為整數
            result = None
            try: result = int(args[0])
            except ValueError:
                # 如果不是，則檢查是否為運算式
                try: result = eval(args[0])
                except: pass
            # 檢查是否為有效參數
            if result == None:
                await raw_message.reply("格式錯誤，請使用`help limit`取得詳細說明。")
                return
            # 如果是，則進行修飾
            result = abs(int(result))
        
        # 則執行指令
        origin_limit = channel.user_limit
        await channel.edit(user_limit=result)
        await raw_message.reply(f"修改成功，已將頻道人數限制由`{origin_limit}`人改為`{channel.user_limit}`人")
        LOG.info(f"Edit channel<{channel.guild.id}/{channel.id}> limit from `{origin_limit}`to `{channel.user_limit}`")
