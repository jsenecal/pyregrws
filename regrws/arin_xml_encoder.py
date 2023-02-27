from enum import Enum
from typing import Any

from pydantic_xml.serializers import XmlEncoder


class ARINXmlEncoder(XmlEncoder):
    def encode(self, obj: Any) -> str:
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, Enum):
            return str(obj.value)
        return super().encode(obj)
