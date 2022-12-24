from configs import DISCORD_CHANNEL, DISCORD_LOGGER as LOG, DISCORD_TOKEN
from configs.config import DISCORD_PREFIXS
import db_operation as dbo
from commands import *

from asyncio import sleep as a_sleep
from typing import Optional

from discord import ApplicationContext, CategoryChannel, Intents, Member, Message, PermissionOverwrite, SlashCommandGroup, VoiceChannel, VoiceState
from discord.abc import GuildChannel
from discord.bot import Bot

def gen_command_template(command: str) -> str:
    return "|".join(map(lambda prefix: f"{prefix}{command}", DISCORD_PREFIXS))

def _not_dvc_embed_generator(author: Member) -> Embed:
    """
    不是動態語音頻道Embed生成器。

    author: :class:`Member`
        作者。

    return: :class:`Embed`
        生成之Embed。
    """
    embed = Embed(
        color=0xff0000,
        title="發生錯誤!",
        description="你不在動態語音頻道內。",
        timestamp=datetime.now(TIMEZONE)
    )
    # 作者
    embed.set_author(
        name=author.display_name,
        icon_url=author.display_avatar.url
    )
    return embed

class DiscordClient(Bot):
    def __init__(self, *args, **kwargs):
        intents = Intents.all()
        super().__init__(*args, **kwargs, intents=intents)

        self.command_group = self.create_group("dvc", guild_ids=[859361081536151573])

        self._dvc_command_init()
    
    def _dvc_command_init(self):
        @self.command_group.command(name="help", description="指令說明")
        async def s_help(app_context: ApplicationContext, command: str):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Help.execute(self.table_name, app_context, (command))
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="name", description="改變你的語音頻道名稱")
        async def s_name(app_context: ApplicationContext, name: str):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Name.execute(self.table_name, app_context, (name,))
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="limit", description="改變頻道限制人數")
        async def s_limit(app_context: ApplicationContext, num: str):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Limit.execute(self.table_name, app_context, (num,))
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="bitrate", description="改變頻道的位元率")
        async def s_bitrate(app_context: ApplicationContext, num: str):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await BitRate.execute(self.table_name, app_context, (num,))
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="hide", description="將語音頻道隱藏，其他使用者無法看見該頻道")
        async def s_hide(app_context: ApplicationContext):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Hide.execute(self.table_name, app_context)
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="unhide", description="將語音頻道設為可見")
        async def s_unhide(app_context: ApplicationContext):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await UnHide.execute(self.table_name, app_context)
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="lock", description="將頻道上鎖，其他使用者無法加入")
        async def s_lock(app_context: ApplicationContext):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Lock.execute(self.table_name, app_context)
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="unlock", description="將頻道解鎖，其他使用者可以加入")
        async def s_unlock(app_context: ApplicationContext):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await UnLock.execute(self.table_name, app_context)
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="kick", description="踢出語音頻道內的某個使用者")
        async def s_kick(app_context: ApplicationContext, tags: str):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Kick.execute(self.table_name, app_context, self._metion_decode(tags))
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="ban", description="驅逐某個使用者")
        async def s_ban(app_context: ApplicationContext, tags: str):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Ban.execute(self.table_name, app_context, self._metion_decode(tags))
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="unban", description="解除驅逐某個使用者")
        async def s_unban(app_context: ApplicationContext, tags: str):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await UnBan.execute(self.table_name, app_context, self._metion_decode(tags))
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="mute", description="禁止所有人說話")
        async def s_mute(app_context: ApplicationContext):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await Mute.execute(self.table_name, app_context)
            await app_context.respond(**ret, ephemeral=True)
        @self.command_group.command(name="unmute", description="允許所有人說話")
        async def s_unmute(app_context: ApplicationContext):
            if app_context.channel.category != self.category: ret = {"embed": _not_dvc_embed_generator(app_context.author)}
            else: ret = await UnMute.execute(self.table_name, app_context)
            await app_context.respond(**ret, ephemeral=True)
    
    def _metion_decode(self, raw_text: str) -> tuple[Member]:
        result = []
        format_list = raw_text.split(">")
        for tag in format_list:
            if "@" not in tag: continue
            try:
                user_id = int(tag.strip("<@!>"))
                member = self.initial_channel.guild.get_member(user_id)
                if member == None: continue
                result.append(member)
            except: continue
        return tuple(member)
    
    async def _add_admin(self, channel: VoiceChannel, member: Member):
        guild = member.guild         # 群組
        table_name = self.table_name # 資料庫表格名稱

        # 開啟權限: 管理頻道、將他人靜音、將他人拒聽、管理訊息
        permission = channel.overwrites_for(member)
        permission.manage_channels = True
        permission.mute_members = True
        permission.deafen_members = True
        permission.manage_messages = True

        # 更新權限
        await channel.set_permissions(member, overwrite=permission)

        # 更新資料庫
        dbo.add_admin(table_name, channel.id, member.id)

        LOG.info(f"Add user<{guild.id}/{member.id}> to channel<{channel.id}> admin.")
    
    async def _remove_admin(self, channel: VoiceChannel, member: Member):
        guild = member.guild         # 群組
        table_name = self.table_name # 資料庫表格名稱

        # 重設權限: 管理頻道、將他人靜音、將他人拒聽、管理訊息
        permission = channel.overwrites_for(member)
        permission.manage_channels = None
        permission.mute_members = None
        permission.deafen_members = None
        permission.manage_messages = None

        # 更新權限
        await channel.set_permissions(member, overwrite=permission)

        # 更新資料庫
        dbo.remove_admin(table_name, channel.id, member.id)

        LOG.info(f"Remove user<{guild.id}/{member.id}> admin from channel<{channel.id}>.")
    
    async def on_ready(self):
        # 取得起始頻道
        self.initial_channel: VoiceChannel = self.get_channel(DISCORD_CHANNEL)
        # 起始頻道所屬之類別
        self.category: Optional[CategoryChannel] = self.initial_channel.category
        if self.category == None:
            self.category = await self.initial_channel.guild.create_category("DVC Category")
            await self.initial_channel.edit(category=self.category)
        # 資料庫表格名稱
        self.table_name = dbo.database_init(self.initial_channel.guild.id)

        LOG.warning(f"Discord Bot `{self.user}` Start.")
    
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        name = member.display_name   # 使用者名稱
        guild = member.guild         # 群組
        l_channel = before.channel   # 離該的頻道
        j_channel = after.channel    # 加入的頻道
        table_name = self.table_name # 資料庫表格名稱

        if l_channel != None:
            l_in_category = l_channel.category == self.category
            if j_channel != None:
                j_in_category = j_channel.category == self.category
                LOG.info(f"User<{guild.id}/{member.id}> <{l_channel.id}> -> <{j_channel.id}>.")
            else:
                j_in_category = False
                LOG.info(f"User<{guild.id}/{member.id}> <{l_channel.id}> -> ")
        else:
            l_in_category = False
            j_in_category = j_channel.category == self.category
            LOG.info(f"User<{guild.id}/{member.id}> -> <{j_channel.id}>")

        # 檢查是否是從起始頻道離開
        if l_channel == self.initial_channel: return
        
        # 檢查是否加入了起始頻道
        if j_channel == self.initial_channel:
            # 創建新頻道
            new_channel = await self.category.create_voice_channel(f"{name} 的語音頻道")
            LOG.info(f"Create channel<{guild.id}/{new_channel.id}>`{new_channel.name}`.")
            # 將使用者移動至該頻道
            await member.move_to(new_channel)

            # 新增資料至資料庫
            dbo.new_channel(table_name, new_channel.id)
            await self._add_admin(new_channel, member)
            return
        
        # 檢查使用者是否為該頻道最後一位離開的管理員
        if j_in_category:
            if dbo.can_claim(table_name, j_channel.id) and member.id == dbo.last_admin(table_name, j_channel.id):
                # 如果是，則恢復其管理員權限
                await self._add_admin(j_channel, member)
                await j_channel.send(f"本頻道原管理員`{member.display_name}`已加回頻道，因此恢復其管理員身分。")
                LOG.info(f"Channel<{guild.id}/{j_channel.id}>`{j_channel.name}` admin return.")
        
        if l_in_category:
            # 檢查離該的頻道內是否還有人
            if len(l_channel.members) == 0:
                # 如果沒有人，則刪除頻道
                await l_channel.delete()
                LOG.info(f"Delete channel<{guild.id}/{l_channel.id}>`{l_channel.name}`.")
            else:
                # 記錄在離開前，頻道內其他人是否可以請求成為管理員
                before_claim = dbo.can_claim(table_name, l_channel.id)
                # 如果離開者是管理員，則將其自管理員清單移除
                await self._remove_admin(l_channel, member)
                # 檢查請求成為管理員權限是否改變
                after_claim = dbo.can_claim(table_name, l_channel.id)
                if after_claim and after != before_claim:
                    # 如果權限改變則開放請求成為新的管理員
                    await l_channel.send(f"由於本頻道原管理員`{member.display_name}`已離開頻道，因此開放其他人請求成為新管理員。\n請使用`{gen_command_template('claim')}`以請求成為新管理員。")
                    LOG.info(f"Channel<{guild.id}/{l_channel.id}>`{l_channel.name}` no admin.")
    
    async def on_guild_channel_create(self, channel: GuildChannel):
        if channel.category != self.category or type(channel) != VoiceChannel: return
        await a_sleep(5)
        # 新增至資料庫
        dbo.new_channel(self.table_name, channel.id)
        # 檢查是否由機器人創建
        if dbo.can_claim(self.table_name, channel.id):
            # 如果否，則開放請求成為管理員之權限
            await channel.send(f"由於本頻道無管理員，因此開放其他人請求成為新管理員。\n請使用`{gen_command_template('claim')}`以請求成為新管理員。")
            LOG.info(f"Channel<{channel.guild.id}/{channel.id}>`{channel.name}` no admin.")

    async def on_guild_channel_delete(self, channel: GuildChannel):
        if channel.category != self.category or type(channel) != VoiceChannel: return
        # 自資料庫移除資料
        dbo.delete_channel(self.table_name, channel.id)
    
    async def on_message(self, message: Message):
        # 檢查是否為無效命令
        if message.author == self.user: return                 # 由自己發出的訊息
        elif message.author.bot: return                        # 由機器人發出的訊息
        elif message.channel.category != self.category: return # 在動態語音類別外的訊息
        elif message.channel == self.initial_channel: return   # 在起始頻道的訊息

        command = message.content.strip().lower() # 修飾指令
        table_name = self.table_name              # 資料庫表格名稱
        # 檢查是否為命令
        if not command.startswith(DISCORD_PREFIXS): return
        # 移除指令前墜
        for preifx in DISCORD_PREFIXS:
            command = command.removeprefix(preifx)
        # 切分指令
        _res = command.split(" ")
        if len(_res) < 2:
            command, args = _res[0], None
        else:
            command, args = _res[0], tuple(_res[1:])
        # 判斷指令
        ret = None
        if command == "help":
            ret = await Help.execute(table_name, message, args)
        if command == "name":
            ret = await Name.execute(table_name, message, args)
        elif command == "limit":
            ret = await Limit.execute(table_name, message, args)
        elif command == "limit":
            ret = await BitRate.execute(table_name, message, args)
        elif command == "hide":
            ret = await Hide.execute(table_name, message, args)
        elif command == "unhide":
            ret = await UnHide.execute(table_name, message, args)
        elif command == "lock":
            ret = await Lock.execute(table_name, message, args)
        elif command == "unlock":
            ret = await UnLock.execute(table_name, message, args)
        elif command == "kick":
            ret = await Kick.execute(table_name, message, args)
        elif command == "ban":
            ret = await Ban.execute(table_name, message, args)
        elif command == "unban":
            ret = await UnBan.execute(table_name, message, args)
        elif command == "mute":
            ret = await Mute.execute(table_name, message, args)
        elif command == "unmute":
            ret = await UnMute.execute(table_name, message, args)
        if ret: await message.reply(**ret)
    
    def run(self, *args, **kwargs) -> None:
        return super().run(DISCORD_TOKEN, *args, **kwargs)

if __name__ == "__main__":
    client = DiscordClient()
    try:
        client.run()
    except KeyboardInterrupt:
        exit()
