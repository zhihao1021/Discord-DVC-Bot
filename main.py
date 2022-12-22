from configs import DISCORD_TOKEN, DISCORD_CHANNEL, DISCORD_LOGGER as LOG

from typing import Optional

from discord import Member, VoiceState, Intents, VoiceChannel, CategoryChannel
from discord.client import Client

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
        member_name = member.display_name
        left_channel = before.channel
        join_channel = after.channel

        if hasattr(left_channel, "id"):
            if hasattr(join_channel, "id"): LOG.info(f"User<{member.id}> move form channel<{left_channel.id}> to channel<{join_channel.id}>.")
            else: LOG.info(f"User<{member.id}> left form channel<{left_channel.id}>.")
        else: LOG.info(f"User<{member.id}> join channel<{join_channel.id}>.")
        
        # 檢查是否加入了起始頻道
        if join_channel == self.initial_channel:
            # 創建新頻道
            new_channel = await join_channel.category.create_voice_channel(f"{member_name} 的語音頻道")
            LOG.info(f"Create channel<{new_channel.id}> named `{new_channel.name}`.")
            # 將使用者移動至該頻道
            member.move_to(new_channel)
            LOG.info(f"Move user<{member.id}> to channel<{new_channel.id}>.")
        
        
        if len(left_channel.members) == 0:
            await left_channel.delete()
    
    def run(self, *args, **kwargs) -> None:
        return super().run(DISCORD_TOKEN, *args, **kwargs)

if __name__ == "__main__":
    client = DiscordClient()
    client.run()