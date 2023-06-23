"""获取用户成绩"""
import aiohttp
from src.maimai_dx.types import BestMaimai


async def best_score(username: str) -> tuple[int, BestMaimai]:
    """从数据库获得用户成绩"""
    async with aiohttp.request("POST",
                               "https://www.diving-fish.com/api/maimaidxprober/query/player",
                               json={"username": username, "b50": True}) as repo:
        if repo.status == 400:
            return [400, None]
        if repo.status == 403:
            return [403, None]
        return [0, BestMaimai(await repo.json())]


if __name__ == "__main__":
    best_score("VinSaruP")
