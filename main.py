from configs import DISCORD_CHANNEL, DISCORD_LOGGER as LOG, DISCORD_TOKEN
from configs.config import DISCORD_PREFIXS
import db_operation as dbo

from typing import Optional

from discord import CategoryChannel, Intents, Member, Message, PermissionOverwrite, VoiceChannel, VoiceState
from discord.client import Client

from modules.json import Json

def gen_command_template(command: str) -> str:
    return "|".join(map(lambda prefix: f"{prefix}{command}", DISCORD_PREFIXS))

class DiscordClient(Client):
    def __init__(self, *args, **kwargs):
        intents = Intents.all()
        super().__init__(*args, **kwargs, intents=intents)
    
    async def on_ready(self):
        LOG.warning(f"Discord Bot `{self.user}` Start.")
        # 取得起始頻道
        self.initial_channel: VoiceChannel = self.get_channel(DISCORD_CHANNEL)
        # 起始頻道所屬之類別
        self.category: Optional[CategoryChannel] = self.initial_channel.category
        if self.category == None:
            self.category = await self.initial_channel.guild.create_category("DVC Category")
            await self.initial_channel.edit(category=self.category)
    
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        name = member.display_name # 使用者名稱
        guild = member.guild       # 群組
        l_channel = before.channel # 離該的頻道
        j_channel = after.channel  # 加入的頻道

        table_name = dbo.database_init(member.guild.id) # 資料庫表格名稱

        if l_channel != None:
            l_in_category = j_channel.category == self.category
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
            dbo.add_admin(table_name, new_channel.id, member.id)
            return
        
        # 檢查使用者是否為該頻道最後一位離開的管理員
        if j_in_category:
            if dbo.can_claim(table_name, j_channel.id) and member.id == dbo.last_admin(table_name, j_channel.id):
                # 如果是，則恢復其管理員權限
                dbo.add_admin(table_name, j_channel.id, member.id)
                await j_channel.send(f"本頻道原管理員`{member.display_name}`已加回頻道，因此恢復其管理員身分。")
                LOG.info(f"Channel<{guild.id}/{j_channel.id}>`{j_channel.name}` admin return.")
        
        if l_in_category:
            # 檢查離該的頻道內是否還有人
            if len(l_channel.members) == 0:
                # 如果沒有人，則刪除頻道
                await l_channel.delete()
                LOG.info(f"Delete channel<{guild.id}/{l_channel.id}>`{l_channel.name}`.")

                # 自資料庫移除資料
                dbo.delete_channel(table_name, l_channel.id)
            else:
                # 記錄在離開前，頻道內其他人是否可以請求成為管理員
                before_claim = dbo.can_claim(table_name, l_channel.id)
                # 如果離開者是管理員，則將其自管理員清單移除
                dbo.remove_admin(table_name, l_channel.id, member.id)
                # 檢查請求成為管理員權限是否改變
                after_claim = dbo.can_claim(table_name, l_channel.id)
                if after_claim and after != before_claim:
                    # 如果權限改變則開放請求成為新的管理員
                    await l_channel.send(f"由於本頻道原管理員`{member.display_name}`已離開頻道，因此開放其他人請求成為新管理員。\n請使用`{gen_command_template('claim')}`以請求成為新管理員。")
                    LOG.info(f"Channel<{guild.id}/{l_channel.id}>`{l_channel.name}` no admin.")
    
    async def on_message(self, message: Message):
        if message.author == self.user: return
    
    def run(self, *args, **kwargs) -> None:
        return super().run(DISCORD_TOKEN, *args, **kwargs)

if __name__ == "__main__":
    client = DiscordClient()
    client.run()