from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

@dataclass
class TranslatableField:
    """表示一个可翻译字段的信息"""
    field_path: str  # 字段路径，如 "content" 或 "conversations.0.value"
    content: str     # 需要翻译的文本内容
    field_type: str  # 字段类型：string, list_item, nested
    index: int = None  # 如果是列表项，记录索引

class FormatHandler(ABC):
    """数据格式处理器基类"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化格式处理器
        
        Args:
            config: 格式配置信息
        """
        self.config = config
        self.name = config.get("name", "unknown")
        self.description = config.get("description", "")
        self.translatable_fields = config.get("translatable_fields", [])
    
    @abstractmethod
    def extract_translatable_content(self, item: Dict[str, Any]) -> List[TranslatableField]:
        """
        从数据项中提取可翻译的内容
        
        Args:
            item: 数据集中的一个数据项
            
        Returns:
            List[TranslatableField]: 可翻译字段列表
        """
        pass
    
    @abstractmethod
    def reconstruct_item(self, item: Dict[str, Any], translated_fields: List[TranslatableField]) -> Dict[str, Any]:
        """
        将翻译后的内容重新组装到数据项中
        
        Args:
            item: 原始数据项
            translated_fields: 翻译后的字段列表
            
        Returns:
            Dict[str, Any]: 重新组装后的数据项
        """
        pass
    
    def validate_item(self, item: Dict[str, Any]) -> bool:
        """
        验证数据项是否符合当前格式
        
        Args:
            item: 要验证的数据项
            
        Returns:
            bool: 是否符合格式要求
        """
        # 基础验证：检查必需字段是否存在
        for field_config in self.translatable_fields:
            if field_config.get("required", False):
                field_name = field_config["field"]
                if field_name not in item:
                    return False
        return True
    
    def get_field_value(self, item: Dict[str, Any], field_path: str) -> Any:
        """
        根据字段路径获取字段值
        
        Args:
            item: 数据项
            field_path: 字段路径，支持嵌套访问如 "conversations.0.value"
            
        Returns:
            Any: 字段值
        """
        parts = field_path.split('.')
        current = item
        
        for part in parts:
            if part.isdigit():
                # 处理数组索引
                index = int(part)
                if isinstance(current, list) and 0 <= index < len(current):
                    current = current[index]
                else:
                    return None
            else:
                # 处理对象键
                if isinstance(current, dict) and part in current:
                    current = current[part]
                else:
                    return None
        
        return current
    
    def set_field_value(self, item: Dict[str, Any], field_path: str, value: Any) -> None:
        """
        根据字段路径设置字段值
        
        Args:
            item: 数据项
            field_path: 字段路径
            value: 要设置的值
        """
        parts = field_path.split('.')
        current = item
        
        # 导航到父对象
        for part in parts[:-1]:
            if part.isdigit():
                index = int(part)
                current = current[index]
            else:
                current = current[part]
        
        # 设置最终值
        final_part = parts[-1]
        if final_part.isdigit():
            index = int(final_part)
            current[index] = value
        else:
            current[final_part] = value
