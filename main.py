"""程序主文件"""
import botpy
from botpy.message import DirectMessage
from botpy.types.message import Message, Reference

from bot_token import BOT_APPID as appid
from bot_token import TOKEN as token
from src.bind import bind_user, show_bind
from src import maimai_dx


# Bot流程：
# 1. 接收信息
# 2. 由command_handle函数处理信息
# 3. 如果是指令则执行相应handle函数


class HananeCli(botpy.Client):
    """服务器类"""
    async def reference(self, content: str, message: Message,
                        file_image: str | bytes = None, reference=False):
        """回复（并引用）消息"""
        await self.api.post_message(channel_id=message.channel_id,
                                    content=content,
                                    msg_id=message.id,
                                    file_image=file_image,
                                    message_reference=Reference(
                                        message_id=message.id)
                                    if reference else None)

    async def dms(self, content: str, message: Message | DirectMessage,
                  file_image: str | bytes = None, from_dms=False, reference=False):
        """私聊信息"""
        if not from_dms:
            private_guild = \
                (await self.api.create_dms(message.guild_id, message.author.id))["guild_id"]
        else:
            private_guild = message.guild_id

        await self.api.post_dms(guild_id=private_guild,
                                content=content,
                                msg_id=message.id,
                                message_reference=Reference(
                                    message_id=message.id) if reference else None,
                                file_image=file_image)

    async def send(self, content: str, message: Message | DirectMessage,
                   file_image: str | bytes = None, from_dms=False, reference=False):
        """发送信息"""
        if from_dms:
            await self.dms(content, message, file_image, from_dms=True, reference=reference)
        else:
            await self.reference(content, message, file_image, reference=reference)

    async def command_handle(self, message: Message | DirectMessage, from_dms=False):
        """信息处理，如果是指令则执行相应handle函数"""
        print(f"接收来自{message.author.username}的信息{message.content}")
        if message.content.startswith("/b50"):
            await self.b50_handle(message, from_dms=from_dms)

        elif message.content.startswith("/bind"):
            await self.bind_handle(message, from_dms=from_dms)

        elif message.content.startswith("/查歌"):
            await self.query_handle(message, from_dms=from_dms)

        elif message.content.startswith("/uid"):
            await self.uid_handle(message, from_dms=from_dms)

        elif message.content == "/创建私聊" and not isinstance(message, DirectMessage):
            await self.dms(message=message, content="Hello!")

    async def b50_handle(self, message: Message, from_dms=False):
        """处理b50指令"""
        if message.content == '/b50':
            username = show_bind(message.author.id)
        else:
            username = message.content[5:]

        if username == "":
            await self.send("未绑定用户名！", message=message,
                            from_dms=from_dms, reference=True)
            return

        status, best_maimai = await maimai_dx.best_score(username)

        if status == 400:
            await self.send(f"用户{username}不存在！", message=message,
                            from_dms=from_dms, reference=True)
            return
        if status == 403:
            await self.send("用户未公开成绩！", message=message,
                            from_dms=from_dms, reference=True)
            return
        await self.send(f"用户{username}的b50成绩为{best_maimai.rating}！",
                        message=message, from_dms=from_dms, reference=True)

    async def bind_handle(self, message: Message, from_dms=False):
        """处理/bind指令"""
        if message.content == '/bind':
            await self.send(f"当前绑定的用户名为: {show_bind(message.author.id)}",
                            message=message, from_dms=from_dms, reference=True)
        elif message.content.startswith('/bind ') and len(message.content) > 6:
            username = message.content[6:]  # startswith '/bind '
            user_id = message.author.id
            bind_user(user_id, username)
            await self.send(f"成功绑定用户名\"{username}\"!", message=message,
                            from_dms=from_dms, reference=True)
        else:
            await self.send("指令错误！", message=message,
                            from_dms=from_dms, reference=True)

    async def query_handle(self, message: Message, from_dms=False):
        """处理查歌指令"""
        if message.content.startswith("/查歌 "):
            tips = message.content[4:]
            await self.send(await maimai_dx.query_music(tips),
                            message=message, from_dms=from_dms, reference=True)

    async def uid_handle(self, message: Message, from_dms=False):
        """根据歌曲uid查询"""
        if message.content.startswith("/uid "):
            uid = message.content[5:]
            music = await maimai_dx.query_music_by_uid(uid)
            await self.send(music.get_info(), file_image=await music.get_cover(),
                            message=message, from_dms=from_dms)

    async def on_at_message_create(self, message: Message):
        """接收at信息"""
        message.content = message.content[message.content.index(" ") + 1:]
        await self.command_handle(message)

    async def on_direct_message_create(self, message: DirectMessage):
        """接收私聊信息"""
        await self.command_handle(message, from_dms=True)


if __name__ == "__main__":
    intents = botpy.Intents.all()
    client = HananeCli(intents=intents)
    client.run(appid=appid, token=token)
