from sqlite3 import connect

def database_init(guild_id: int) -> str:
    """
    檢查檢查該群組之表格是否存在，若不存在則創建一個新表格。

    guild_id: :class:`int`
        群組ID。

    return: :class:`str`
        該群組表格之名稱。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    name = f"guild-{guild_id}"
    cursor.execute("SELECT name FROM sqlite_master WHERE type=\"table\" AND name=$1", (name,))
    result = cursor.fetchone()
    if result == None:
        # 如果該表格不存在
        cursor.execute(f"""
            CREATE TABLE \"{name}\" (
                "channel_id"	INTEGER NOT NULL UNIQUE,
                "admin_list"	TEXT NOT NULL DEFAULT "[]",
                "ban_list"	TEXT NOT NULL DEFAULT "[]",
                "no_admin"	BLOB NOT NULL DEFAULT 1,
                "last_admin"	INTEGER,
                PRIMARY KEY("channel_id")
            )
        """)
        db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()

    return name

def new_channel(table_name: str, channel_id: int) -> None:
    """
    新增頻道資料。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 檢查資料是否已經存在
    cursor.execute(f"SELECT channel_id FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    if cursor.fetchone() != None: return
    # 新增資料
    cursor.execute(f"INSERT INTO \"{table_name}\" (channel_id) VALUES ($1)", (channel_id,))
    db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()

def delete_channel(table_name: str, channel_id: int) -> None:
    """
    刪除頻道資料。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 移除資料
    cursor.execute(f"DELETE FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()

def can_claim(table_name: str, channel_id: int) -> bool:
    """
    檢查該頻道是否能夠請求成為管理員。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    
    return: :class:`bool`
        是否能夠請求成為管理員。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 檢查頻道內是否還有管理員
    cursor.execute(f"SELECT no_admin FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    result = bool(cursor.fetchone()[0])

    # 關閉資料庫
    cursor.close()
    db.close()

    return result

def set_claim(table_name: str, channel_id: int, can_claim: bool) -> None:
    """
    設置該頻道是否能夠請求成為管理員。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    can_claim: :class:`bool`
        設置為是/否能夠請求成為管理員。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 檢查頻道內是否還有管理員
    cursor.execute(f"UPDATE \"{table_name}\" SET no_admin=$1 WHERE channel_id=$2", (int(can_claim), channel_id,))
    db.commit()

    # 關閉資料庫
    cursor.close()
    db.close()

def last_admin(table_name: str, channel_id: int) -> int:
    """
    該頻道上一位離開的管理員。

    table_name: :class:`str`
        該群組表格之名稱。
    channel_id: :class:`int`
        頻道ID。
    
    return: :class:`int`
        該頻道上一位離開的管理員ID。
    """
    # 連接至資料庫
    db = connect("data.db")
    cursor = db.cursor()

    # 取得資料
    cursor.execute(f"SELECT last_admin FROM \"{table_name}\" WHERE channel_id=$1", (channel_id,))
    result = cursor.fetchone()
    if result != None: result = result[0]

    # 關閉資料庫
    cursor.close()
    db.close()

    return result
