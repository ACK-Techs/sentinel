"""基础命令类"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseCommand(ABC):
    """基础命令类"""
    
    def __init__(self, name: str, description: str, alt_name: Optional[str] = None):
        self.name = name
        self.description = description
        self.alt_name = alt_name
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any], args: str) -> dict:
        """执行命令"""
        pass
