
from typing import Any, Optional, Union
try:
    import orjson

    class Json:
        """
        基於orjson的改良版本。
        """
        @staticmethod
        def dumps(data: Any,
            option: Optional[int]=None
        ) -> str:
            """
            將`data`轉換為字串。
            
            data: :class:`Any`
                輸入資料。
            option: :class:`int`
                orjson選項。

            return: :class:`str`
            """
            if option != None: return orjson.dumps(data, option=option).decode('utf-8')
            return orjson.dumps(data).decode('utf-8')

        @staticmethod
        def loads(data: Union[bytes, bytearray, memoryview, str]) -> Any:
            """
            將`data`轉換為資料。
            
            data: :class:`bytes | bytearray | memoryview | str`
                輸入文字。

            return: :class:`Any`
            """
            return orjson.loads(data)

        @staticmethod
        def dump(
            file: str,
            data: Any,
            option: int = orjson.OPT_INDENT_2
        ) -> None:
            """
            將`data`儲存於`file`中。
            
            file: :class:`str`
                文件路徑。
            data: :class:`Any`
                輸入資料。
            option: :class:`int`
                orjson選項。

            return: :class:`None`
            """
            open(file, mode="wb").write(orjson.dumps(data, option=option))

        @staticmethod
        def load(file: str) -> Any:
            """
            從`file`中讀取資料。
            
            file: :class:`str`
                文件路徑。

            return: :class:`Any`
            """
            return orjson.loads(open(file, mode="rb").read().decode("utf-8"))
except:
    import json

    class Json:
        """
        基於orjson的改良版本。
        """
        @staticmethod
        def dumps(data: Any) -> str:
            """
            將`data`轉換為字串。

            data: :class:`Any`
                輸入資料。
            option: :class:`int`
                orjson選項。

            return: :class:`str`
            """
            return json.dumps(data, sort_keys=False)

        @staticmethod
        def loads(data: Union[bytes, bytearray, memoryview, str]) -> Any:
            """
            將`data`轉換為資料。

            data: :class:`bytes | bytearray | memoryview | str`
                輸入文字。

            return: :class:`Any`
            """
            return json.loads(data)

        @staticmethod
        def dump(
            file: str,
            data: Any,
        ) -> None:
            """
            將`data`儲存於`file`中。

            file: :class:`str`
                文件路徑。
            data: :class:`Any`
                輸入資料。
            option: :class:`int`
                orjson選項。

            return: :class:`None`
            """
            json.dump(data, open(file, mode="w"))

        @staticmethod
        def load(file: str) -> Any:
            """
            從`file`中讀取資料。

            file: :class:`str`
                文件路徑。

            return: :class:`Any`
            """
            return json.load(open(file, mode="r"))
