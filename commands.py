from configs import DISCORD_PREFIXS, DISCORD_LOGGER as LOG, TIMEZONE
import db_operation as dbo

from datetime import datetime
from typing import Optional

from discord import Member, Message, VoiceChannel, Embed

def _is_admin(table_name: str, channel: VoiceChannel, user: Member) -> bool:
    """
    檢查使用者是否為該頻道之管理員。

    table_name: :class:`str`
        該群組表格之名稱。
    channel: :class:`VoiceChannel`
        該頻道。
    user: :class:`Member`
        使用者。

    return: :class:`bool`
        是否為管理員。
    """
    # 取得管理員清單
    admin_list = dbo.get_admin(table_name, channel.id)
    # 檢查是否為管理員
    if user.id not in admin_list:
        # 如果不是管理員
        return False
    # 如果是管理員
    return True

def _help_embed_generator(
    author: Member,
    title: str,
    format_: str,
    intro: list[str],
    args: list[str],
    example: list[str]
) -> Embed:
    """
    幫助Embed生成器。

    author: :class:`Member`
        作者。
    title: :class:`str`
        指令名稱。
    format_: :class:`str`
        指令格式。
    intro: :class:`list[str]`
        指令說明。
    args: :class:`list[str]`
        指令參數說明。
    example: :class:`list[str]`
        指令範例。

    return: :class:`Embed`
        生成之Embed。
    """
    _e_prefix = DISCORD_PREFIXS[0] # 指令開頭
    embed = Embed(
        color=0xffc800,
        title=f"指令說明 - `{title}`",
        timestamp=datetime.now(TIMEZONE),
    )
    embed.description = "\n".join([
        f"指令有效開頭:`{'|'.join(DISCORD_PREFIXS)}`",
        f"格式 - `{format_}`",
    ])
    # 指令說明
    intro = map(lambda in_str: f"> {in_str}", intro)
    embed.add_field(name="說明", value="\n".join(intro), inline= False)
    if len(args) != 0:
        # 指令參數說明
        args = map(lambda in_str: f"> {in_str}", args)
        embed.add_field(name="參數", value="\n".join(args), inline= False)
    # 指令範例
    example = map(lambda in_str: f"> `{_e_prefix}{in_str}`", example)
    embed.add_field(name="範例", value="\n".join(example), inline= False)
    # 作者
    embed.set_author(
        name=author.display_name,
        icon_url=author.display_avatar.url
    )
    return embed

def _not_admin_embed_generator(author: Member) -> Embed:
    """
    不是管理員Embed生成器。

    author: :class:`Member`
        作者。

    return: :class:`Embed`
        生成之Embed。
    """
    embed = Embed(
        color=0xff0000,
        title="發生錯誤!",
        description="你不是本頻道的管理員。",
        timestamp=datetime.now(TIMEZONE)
    )
    # 作者
    embed.set_author(
        name=author.display_name,
        icon_url=author.display_avatar.url
    )
    return embed

def _format_error_embed_generator(author: Member, command: str) -> Embed:
    """
    格式錯誤Embed生成器。

    author: :class:`Member`
        作者。
    command: :class:`str`
        指令。

    return: :class:`Embed`
        生成之Embed。
    """
    embed = Embed(
        color=0xff0000,
        title="發生錯誤!",
        description=f"格式錯誤，請使用`help {command}`取得詳細說明。",
        timestamp=datetime.now(TIMEZONE)
    )
    # 作者
    embed.set_author(
        name=author.display_name,
        icon_url=author.display_avatar.url
    )
    return embed

def _success_embed_generator(author: Member, message: str) -> Embed:
    """
    執行成功Embed生成器。

    author: :class:`Member`
        作者。
    message: :class:`str`
        成功訊息。

    return: :class:`Embed`
        生成之Embed。
    """
    embed = Embed(
        color=0x00ff00,
        title="命令執行成功",
        description=message,
        timestamp=datetime.now(TIMEZONE)
    )
    # 作者
    embed.set_author(
        name=author.display_name,
        icon_url=author.display_avatar.url
    )
    return embed

class BaseCommand:
    @staticmethod
    async def help(raw_message: Message) -> dict:
        raise NotImplementedError
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        raise NotImplementedError

class Help(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        author = raw_message.author # 訊息發送者
        embed = Embed(
            color=0xffc800,
            title="指令說明 - `help`",
            timestamp=datetime.now(TIMEZONE),
        )
        embed.description = "\n".join([
            f"指令有效開頭:`{'|'.join(DISCORD_PREFIXS)}`",
            f"可使用`help <command>`獲得詳細說明",
        ])
        embed.add_field(name="基礎設定", value="\n".join([
            f"> `name <name>`   - 改變你的語音頻道名稱",
            f"> `limit <num>`   - 改變頻道限制人數",
            f"> `bitrate <num>` - 改變頻道的位元率",
        ]), inline= False)
        embed.add_field(name="隱私相關設定", value="\n".join([
            f"> `hide`   - 將語音頻道隱藏，其他使用者無法看見該頻道",
            f"> `unhide` - 將語音頻道設為可見",
            f"> `lock`   - 將頻道上鎖，其他使用者無法加入",
            f"> `unlock` - 將頻道解鎖，其他使用者可以加入",
        ]), inline= False)
        embed.add_field(name="管理參與者", value="\n".join([
            f"> `kick <tag>`  - 踢出語音頻道內的某個使用者",
            f"> `ban <tag>`   - 驅逐某個使用者",
            f"> `unban <tag>` - 解除驅逐某個使用者",
        ]), inline= False)
        embed.add_field(name="管理頻道", value="\n".join([
            f"> `mute`              - 禁止所有人說話",
            f"> `unmute`            - 允許所有人說話",
            f"> `chmod <mod> <tag>` - 管理個別使用者之權限",
        ]), inline= False)
        embed.set_author(
            name=author.display_name,
            icon_url=author.display_avatar.url
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(tabel_nam: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        if args[0] == "name":
            return await Name.help(raw_message)
        elif args[0] == "limit":
            return await Limit.help(raw_message)
        elif args[0] == "bitrate":
            return await BitRate.help(raw_message)
        elif args[0] == "hide":
            return await Hide.help(raw_message)
        elif args[0] == "unhide":
            return await UnHide.help(raw_message)
        elif args[0] == "lock":
            return await Lock.help(raw_message)
        elif args[0] == "unlock":
            return await UnLock.help(raw_message)
        elif args[0] == "kick":
            return await Kick.help(raw_message)
        elif args[0] == "ban":
            return await Ban.help(raw_message)
        elif args[0] == "unban":
            return await UnBan.help(raw_message)
        else:
            return await Help.help(raw_message)

class Name(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道名稱更改為`<name>`。",
        ]
        # 指令參數說明
        args = [
            "`<name>` - 字串，新的頻道名稱。",
        ]
        # 指令範例
        example = [
            "name New_Channel_Name",
            "name new name",
        ]
        embed = _help_embed_generator(
            author=author,
            title="name",
            format_="name <name>",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}

        # 檢查是否有參數傳入
        if args == None or len(args) < 1:
            return {"embed": _format_error_embed_generator(author, "name")}

        # 執行指令
        origin_name = channel.name
        new_name = " ".join(args)
        await channel.edit(name=new_name)
        LOG.info(f"Edit channel<{channel.guild.id}/{channel.id}> name from `{origin_name}` to `{channel.name}`.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道名稱由`{origin_name}`改為`{channel.name}`。"
        )}

class Limit(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道人數上限更改為`<num>`人。",
        ]
        # 指令參數說明
        args = [
            "`<num>` - 整數或運算式，人數上限。",
        ]
        # 指令範例
        example = [
            "limit 10",
            "limit (7+8*6)/5-1",
        ]
        embed = _help_embed_generator(
            author=author,
            title="limit",
            format_="limit <num>",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 檢查是否有參數傳入
        if args == None or len(args) < 1:
            return {"embed": _format_error_embed_generator(author, "limit")}
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
                return {"embed": _format_error_embed_generator(author, "limit")}
            # 如果是，則進行修飾
            result = abs(int(result))
        
        # 則執行指令
        origin_limit = channel.user_limit
        await channel.edit(user_limit=result)
        LOG.info(f"Edit channel<{channel.guild.id}/{channel.id}> limit from `{origin_limit}`to `{channel.user_limit}`.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道人數限制由`{origin_limit}`人改為`{channel.user_limit}`人。"
        )}

class BitRate(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道位元率更改為`<num>`kbps。",
        ]
        # 指令參數說明
        args = [
            "`<num>` - 整數或運算式，位元率。",
        ]
        # 指令範例
        example = [
            "limit 64",
            "limit 8**3/8",
        ]
        embed = _help_embed_generator(
            author=author,
            title="bitrate",
            format_="bitrate <num>",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 檢查是否有參數傳入
        if args == None or len(args) < 1:
            return {"embed": _format_error_embed_generator(author, "bitrate")}
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
                return {"embed": _format_error_embed_generator(author, "bitrate")}
            # 如果是，則進行修飾
            result = max(int(result), 8)
            result = min(96, result)
        
        # 則執行指令
        origin_bitrate = channel.bitrate
        await channel.edit(bitrate=result)
        LOG.info(f"Edit channel<{channel.guild.id}/{channel.id}> bitrate from `{origin_bitrate}kbps`to `{channel.bitrate}kbps`.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道位元率由`{origin_bitrate}kbps`改為`{channel.bitrate}kbps`。"
        )}

class Hide(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道隱藏，其他使用者將無法看到本頻道。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "hide",
        ]
        embed = _help_embed_generator(
            author=author,
            title="hide",
            format_="hide",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        everyone_role = channel.guild.default_role
        await channel.set_permissions(everyone_role, view_channel=False)
        LOG.info(f"Hide channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道隱藏。"
        )}

class UnHide(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道解除隱藏，其他使用者將可以看到本頻道。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "unhide",
        ]
        embed = _help_embed_generator(
            author=author,
            title="unhide",
            format_="unhide",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        everyone_role = channel.guild.default_role
        await channel.set_permissions(everyone_role, view_channel=None)
        LOG.info(f"Unhide channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道取消隱藏。"
        )}

class Lock(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道上鎖，其他使用者將無法連接至本頻道。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "lock",
        ]
        embed = _help_embed_generator(
            author=author,
            title="lock",
            format_="lock",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        everyone_role = channel.guild.default_role
        await channel.set_permissions(everyone_role, connect=False)
        LOG.info(f"Lock channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道上鎖。"
        )}

class UnLock(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道解鎖，其他使用者將無法連接至本頻道。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "unlock",
        ]
        embed = _help_embed_generator(
            author=author,
            title="unlock",
            format_="unlock",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        everyone_role = channel.guild.default_role
        await channel.set_permissions(everyone_role, connect=None)
        LOG.info(f"Unlock channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道解鎖。"
        )}

class Kick(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將使用者從頻道中踢出。",
            "備註:只要有被Tag到的使用者都會被踢出。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "kick <@302774180611358720>",
            "kick <@302774180611358720> <@859360640626589696> <@844207119296364594>",
        ]
        embed = _help_embed_generator(
            author=author,
            title="kcik",
            format_="kick <@tag>",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        if hasattr(raw_message, "mentions"): members = raw_message.mentions
        else: members = args
        for member in members:
            await member.move_to(None)
        members_name = [f"`{member.display_name}`" for member in members]
        members_log = [f"user<{member.id}>" for member in members]
        LOG.info(f"Kick {','.join(members_log)} from channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"執行成功，已將{'、'.join(members_name)}自頻道踢出。"
        )}

class Ban(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將使用者從頻道中驅逐，在解除驅逐以前皆無法再次連接至頻道。",
            "備註:只要有被Tag到的使用者都會被驅逐。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "ban <@302774180611358720>",
            "ban <@302774180611358720> <@859360640626589696> <@844207119296364594>",
        ]
        embed = _help_embed_generator(
            author=author,
            title="ban",
            format_="ban <@tag>",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        if hasattr(raw_message, "mentions"): members = raw_message.mentions
        else: members = args
        for member in members:
            if member == author:
                await raw_message.reply("你無法驅逐你自己。")
                members.remove(member)
                continue
            await member.move_to(None)
            await channel.set_permissions(member,
                read_message_history=False,
                send_messages=False,
                connect=False,
                view_channel=False
            )
        members_name = [f"`{member.display_name}`" for member in members]
        members_log = [f"user<{member.id}>" for member in members]
        LOG.info(f"Ban {','.join(members_log)} from channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"執行成功，已將{'、'.join(members_name)}自頻道驅逐。"
        )}

class UnBan(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將解除驅逐使用者。",
            "備註:只要有被Tag到的使用者都會被解除驅逐。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "unban <@302774180611358720>",
            "unban <@302774180611358720> <@859360640626589696> <@844207119296364594>",
        ]
        embed = _help_embed_generator(
            author=author,
            title="unban",
            format_="unban <@tag>",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        if hasattr(raw_message, "mentions"): members = raw_message.mentions
        else: members = args
        for member in members:
            await channel.set_permissions(member,
                read_message_history=None,
                send_messages=None,
                connect=None,
                view_channel=None
            )
        members_name = [f"`{member.display_name}`" for member in members]
        members_log = [f"user<{member.id}>" for member in members]
        LOG.info(f"Unban {','.join(members_log)} from channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"執行成功，已將{'、'.join(members_name)}自頻道解除驅逐。"
        )}

class Mute(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道靜音，所有使用者將無法說話。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "mute",
        ]
        embed = _help_embed_generator(
            author=author,
            title="mute",
            format_="mute",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        everyone_role = channel.guild.default_role
        await channel.set_permissions(everyone_role, speak=False)
        LOG.info(f"Mute channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道靜音。"
        )}

class UnMute(BaseCommand):
    @staticmethod
    async def help(raw_message: Message) -> dict:
        # 訊息發送者
        author = raw_message.author
        # 指令說明
        intro = [
            "將頻道取消靜音，所有使用者將可以說話。",
        ]
        # 指令參數說明
        args = []
        # 指令範例
        example = [
            "unmute",
        ]
        embed = _help_embed_generator(
            author=author,
            title="unmute",
            format_="unmute",
            intro=intro,
            args=args,
            example=example,
        )
        return {"embed": embed}
    
    @staticmethod
    async def execute(table_name: str, raw_message: Message, args: Optional[tuple]=None) -> dict:
        channel = raw_message.channel # 頻道
        author = raw_message.author   # 訊息發送者
        # 檢查是否為管理員
        if not _is_admin(table_name, channel, author):
            return {"embed": _not_admin_embed_generator(author)}
        
        # 則執行指令
        everyone_role = channel.guild.default_role
        await channel.set_permissions(everyone_role, speak=None)
        LOG.info(f"Unmute channel<{channel.guild.id}/{channel.id}>.")
        return {"embed": _success_embed_generator(
            author=author,
            message=f"修改成功，已將頻道取消靜音。"
        )}
