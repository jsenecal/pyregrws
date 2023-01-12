from typing import Any	

from pydantic_xml.serializers import XmlEncoder	


class ARINXmlEncoder(XmlEncoder):	
    def encode(self, obj: Any) -> str:	
        if isinstance(obj, bool):	
            return "true" if obj else "false"
        return super().encode(obj)	