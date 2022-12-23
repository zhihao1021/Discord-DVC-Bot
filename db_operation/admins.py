from sqlite3 import connect
from modules import Json

def get_admin(table_name: str, channel_id: int) -> list[int]:
    """
    取得該頻道管理員之列表。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    
    return: :class:`list[int]`
        管理員清單。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 取得表格
    cursor.execute(f"SELECT admin_list FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    admin_list: list[int] = Json.loads(cursor.fetchone()[0])

    # 關閉資料庫
    cursor.close()
    db.close()

    return admin_list

def add_admin(table_name: str, channel_id: int, user_id: int) -> None:
    """
    將使用者新增至該頻道之管理員。

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
    cursor.execute(f"SELECT admin_list FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    admin_list: list = Json.loads(cursor.fetchone()[0])
    # 將使用者加入清單
    if user_id not in admin_list: admin_list.append(user_id)
    cursor.execute(f"UPDATE \"{table_name}\" SET admin_list=$1, no_admin=0 WHERE channel_id=$2", (Json.dumps(admin_list), channel_id,))
    db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()

def remove_admin(table_name: str, channel_id: int, user_id: int) -> None:
    """
    移除該使用者於頻道之管理員。

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
    cursor.execute(f"SELECT admin_list FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    admin_list: list = Json.loads(cursor.fetchone()[0])
    # 將使用者自清單移除
    if user_id in admin_list:
        admin_list.remove(user_id)
        cursor.execute(f"UPDATE \"{table_name}\" SET last_admin=$1 WHERE channel_id=$2", (user_id, channel_id,))
    # 檢查頻道內是否還有管理員
    no_admin = len(admin_list) == 0
    cursor.execute(f"UPDATE \"{table_name}\" SET admin_list=$1, no_admin=$2 WHERE channel_id=$3",(
        Json.dumps(admin_list), # 管理員清單
        int(no_admin),          # 是否有管理員
        channel_id,
                     # 頻道ID
    ))
    db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()