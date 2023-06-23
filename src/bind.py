"""bind指令模块"""
import json


FP = "database/username.json"  # 用户名储存位置，如果使用数据库记得把下面的也改了
user_excel = dict()


with open(FP, "r", encoding="utf-8") as excel_file_read:
    user_excel = json.load(excel_file_read)


def bind_user(user_id: str, username: str) -> None:
    """绑定用户"""
    user_excel[user_id] = username
    with open(FP, "w", encoding="utf-8") as excel_file_write:
        excel_file_write.write(json.dumps(user_excel))


def show_bind(user_id: str) -> str:
    """返回绑定的用户名"""
    try:
        return user_excel[user_id]
    except KeyError:
        return ""


if __name__ == "__main__":
    print(user_excel)
