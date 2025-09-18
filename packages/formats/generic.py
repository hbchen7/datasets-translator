from typing import Dict, List, Any
from .base import FormatHandler, TranslatableField

class GenericFormatHandler(FormatHandler):
    """通用格式处理器，基于配置文件处理任意格式"""
    
    def extract_translatable_content(self, item: Dict[str, Any]) -> List[TranslatableField]:
        """从数据项中提取可翻译的内容"""
        translatable_content = []
        
        for field_config in self.translatable_fields:
            field_name = field_config["field"]
            field_type = field_config.get("type", "string")
            
            if field_name not in item:
                continue
                
            if field_type == "string":
                # 处理简单字符串字段
                content = item[field_name]
                if content and isinstance(content, str):
                    translatable_content.append(
                        TranslatableField(
                            field_path=field_name,
                            content=content,
                            field_type="string"
                        )
                    )
            
            elif field_type == "list":
                # 处理列表字段
                list_content = item[field_name]
                if isinstance(list_content, list):
                    sub_fields = field_config.get("sub_fields", [])
                    
                    for i, list_item in enumerate(list_content):
                        if isinstance(list_item, dict):
                            # 列表中的对象
                            for sub_field in sub_fields:
                                sub_field_name = sub_field["field"]
                                if sub_field_name in list_item:
                                    content = list_item[sub_field_name]
                                    if content and isinstance(content, str):
                                        # 检查条件过滤（如ShareGPT格式的role过滤）
                                        condition = sub_field.get("condition")
                                        if condition and not self._check_condition(list_item, condition):
                                            continue
                                            
                                        field_path = f"{field_name}.{i}.{sub_field_name}"
                                        translatable_content.append(
                                            TranslatableField(
                                                field_path=field_path,
                                                content=content,
                                                field_type="list_item",
                                                index=i
                                            )
                                        )
                        elif isinstance(list_item, str):
                            # 列表中的字符串
                            field_path = f"{field_name}.{i}"
                            translatable_content.append(
                                TranslatableField(
                                    field_path=field_path,
                                    content=list_item,
                                    field_type="list_item",
                                    index=i
                                )
                            )
        
        return translatable_content
    
    def reconstruct_item(self, item: Dict[str, Any], translated_fields: List[TranslatableField]) -> Dict[str, Any]:
        """将翻译后的内容重新组装到数据项中"""
        # 创建深拷贝避免修改原始数据
        import copy
        result_item = copy.deepcopy(item)
        
        for field in translated_fields:
            self.set_field_value(result_item, field.field_path, field.content)
        
        return result_item
    
    def _check_condition(self, item: Dict[str, Any], condition: str) -> bool:
        """
        检查条件过滤
        
        Args:
            item: 要检查的数据项
            condition: 条件字符串，格式如 "role:human|assistant" 或 "type:user"
            
        Returns:
            bool: 是否满足条件
        """
        if ":" not in condition:
            return True
            
        field_name, expected_values = condition.split(":", 1)
        if field_name not in item:
            return False
            
        actual_value = item[field_name]
        expected_list = expected_values.split("|")
        
        return actual_value in expected_list
