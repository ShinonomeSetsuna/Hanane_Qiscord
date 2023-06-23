"""自定义数据类型"""
from typing import TypedDict
import aiohttp


class MusicScore(TypedDict):
    """MusicScore Type"""
    title: str
    song_id: str
    ds: float
    type: str
    # 乐曲成绩
    achievements: float
    dxScore: int
    fc: str
    fs: str
    ra: float
    rate: str
    # 乐曲难度
    level: str
    level_label: int
    level_index: str


class BestMaimai:
    """自定义用户成绩格式"""

    def __init__(self, score_json: dict):
        self.username = score_json["username"]
        self.nickname = score_json["nickname"]
        self.rating = score_json["rating"]
        self.b35: list[MusicScore] = [MusicScore(
            i) for i in score_json["charts"]["sd"]]
        self.b15: list[MusicScore] = [MusicScore(
            i) for i in score_json["charts"]["dx"]]


class MusicObject:
    """"""


class Music:
    """自定义乐曲格式"""

    def __init__(self, data: dict) -> None:
        # 乐曲信息
        self.uid = data["id"]
        self.int = int(self.uid)
        self.title = data["title"]
        self.type = data["type"]
        self.real_level = data["ds"]
        # 乐曲难度
        self.level = data["level"]
        self.cids = data["cids"]
        self.charts = data["charts"]
        # 乐曲基本信息
        self.basic_info = data["basic_info"]

    def __str__(self) -> str:
        return f"{self.uid}. {self.title}"

    def get_info(self) -> str:
        """获取乐曲信息"""
        return f"{self.title}\n" + \
            "\n".join([f"{i}: {self.basic_info[i]}" for i in self.basic_info])

    def get_uid(self) -> str:
        """对uid进行换算"""
        return f"{(self.int if (self.int < 11000 and self.int > 10000) else self.int):05d}"

    async def get_cover(self) -> bytes:
        """获取乐曲封面"""
        async with aiohttp.request("GET",
                                   f"https://www.diving-fish.com/covers/{self.get_uid()}.png") \
                as repo:
            return await repo.read()
