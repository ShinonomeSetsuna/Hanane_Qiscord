"""查询歌曲"""

import aiohttp
from src.maimai_dx.types import Music


async def query_music(tips: str) -> str:
    """查询歌曲"""
    async with aiohttp.request("GET",
                               "https://www.diving-fish.com/api/maimaidxprober/music_data") as repo:
        if repo.status == 200:
            total_list = [Music(i) for i in (await repo.json())]
        result: list[Music] = []
        for music in total_list:
            if tips.lower() in music.title.lower():
                result.append(music)
        if len(result) == 0:
            return "未找到相关乐曲！"
        if len(result) > 10:
            return "结果过多，请输入更精确的关键词！"
        return "您要查找的乐曲可能是: \n" + "\n".join([f"{i.uid}. {i.title}" for i in result])


async def query_music_by_uid(uid: int) -> Music:
    """通过uid查询歌曲"""
    async with aiohttp.request("GET",
                               "https://www.diving-fish.com/api/maimaidxprober/music_data") as repo:
        if repo.status == 200:
            total_list = [Music(i) for i in (await repo.json())]
        for music in total_list:
            if music.uid == uid:
                return music
        return None
