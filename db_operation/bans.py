from sqlite3 import connect
from modules import Json

def get_ban(table_name: str, channel_id: int) -> list[int]:
    """
    取得該頻道封禁之列表。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    
    return: :class:`list[int]`
        被封禁者清單。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 取得表格
    cursor.execute(f"SELECT ban_list FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    ban_list: list[int] = Json.loads(cursor.fetchone()[0])

    # 關閉資料庫
    cursor.close()
    db.close()

    return ban_list

def add_ban(table_name: str, channel_id: int, user_id: int) -> None:
    """
    將使用者新增至該頻道之封禁列表。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    user_id: :class:`int`
        使用者ID。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 取得表格
    cursor.execute(f"SELECT ban_list FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    ban_list: list = Json.loads(cursor.fetchone()[0])
    # 將使用者加入清單
    if user_id not in ban_list: ban_list.append(user_id)
    cursor.execute(f"UPDATE \"{table_name}\" SET ban_list=$1 WHERE channel_id=$2", (Json.dumps(ban_list), channel_id,))
    db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()

def remove_ban(table_name: str, channel_id: int, user_id: int) -> None:
    """
    移除該使用者於該頻道之封禁。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    user_id: :class:`int`
        使用者ID。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 取得表格
    cursor.execute(f"SELECT ban_list FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    ban_list: list = Json.loads(cursor.fetchone()[0])
    # 將使用者自清單移除
    if user_id in ban_list: ban_list.remove(user_id)
    cursor.execute(f"UPDATE \"{table_name}\" SET ban_list=$1 WHERE channel_id=$2", (Json.dumps(ban_list), channel_id,))
    db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()