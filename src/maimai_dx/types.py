"""自定义数据类型"""
import aiohttp


class MusicScore:
    """自定义乐曲格式"""

    def __init__(self, data: dict) -> None:
        # 乐曲信息
        self.title = data["title"]
        self.song_id = data["song_id"]
        self.real_level = data["ds"]
        self.type = data["type"]
        # 乐曲成绩
        self.achievement = data["achievements"]
        self.dx_score = data["dxScore"]
        self.rating = data["ra"]
        self.rate = data["rate"]
        self.full_combo = data["fc"]
        self.full_sync = data["fs"]
        # 乐曲难度
        self.level = data["level"]
        self.level_label = data["level_label"]
        self.level_index = data["level_index"]


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

    async def get_cover(self) -> bytes:
        """获取乐曲封面"""
        async with aiohttp.request("GET",
                                   f"https://www.diving-fish.com/covers/{(self.int if (self.int < 11000 and self.int > 10000) else self.int):05d}.png") as repo:
            return await repo.read()
