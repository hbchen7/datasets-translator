import os
import yaml
from typing import Dict, Any, List, Optional
from .formats.base import FormatHandler
from .formats.generic import GenericFormatHandler

class ConfigManager:
    """配置管理器，负责加载和管理格式配置"""
    
    def __init__(self, config_dir: str = "configs"):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置文件目录路径
        """
        self.config_dir = config_dir
        self._configs = {}
        self._load_configs()
    
    def _load_configs(self):
        """加载所有配置文件"""
        if not os.path.exists(self.config_dir):
            raise FileNotFoundError(f"Config directory '{self.config_dir}' not found")
        
        for filename in os.listdir(self.config_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                config_name = os.path.splitext(filename)[0]
                config_path = os.path.join(self.config_dir, filename)
                
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = yaml.safe_load(f)
                        self._configs[config_name] = config
                        print(f"Loaded config: {config_name}")
                except Exception as e:
                    print(f"Error loading config '{filename}': {str(e)}")
    
    def get_config(self, format_name: str) -> Dict[str, Any]:
        """
        获取指定格式的配置
        
        Args:
            format_name: 格式名称
            
        Returns:
            Dict[str, Any]: 格式配置
            
        Raises:
            KeyError: 如果格式不存在
        """
        if format_name not in self._configs:
            raise KeyError(f"Format '{format_name}' not found. Available formats: {list(self._configs.keys())}")
        
        return self._configs[format_name]
    
    def list_formats(self) -> List[str]:
        """
        列出所有可用的格式
        
        Returns:
            List[str]: 格式名称列表
        """
        return list(self._configs.keys())
    
    def create_format_handler(self, format_name: str) -> FormatHandler:
        """
        创建格式处理器实例
        
        Args:
            format_name: 格式名称
            
        Returns:
            FormatHandler: 格式处理器实例
        """
        config = self.get_config(format_name)
        return GenericFormatHandler(config)
    
    def detect_format(self, sample_data: Dict[str, Any]) -> Optional[str]:
        """
        自动检测数据格式
        
        Args:
            sample_data: 数据样本
            
        Returns:
            Optional[str]: 检测到的格式名称，如果无法确定则返回None
        """
        for format_name, config in self._configs.items():
            handler = GenericFormatHandler(config)
            if handler.validate_item(sample_data):
                return format_name
        
        return None
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        验证配置文件的有效性
        
        Args:
            config: 配置字典
            
        Returns:
            bool: 配置是否有效
        """
        required_fields = ["name", "translatable_fields"]
        
        for field in required_fields:
            if field not in config:
                return False
        
        # 验证translatable_fields结构
        translatable_fields = config["translatable_fields"]
        if not isinstance(translatable_fields, list):
            return False
        
        for field_config in translatable_fields:
            if not isinstance(field_config, dict) or "field" not in field_config:
                return False
        
        return True
    
    def reload_configs(self):
        """重新加载所有配置文件"""
        self._configs.clear()
        self._load_configs()
    
    def add_config_from_dict(self, format_name: str, config: Dict[str, Any]):
        """
        从字典添加配置
        
        Args:
            format_name: 格式名称
            config: 配置字典
        """
        if not self.validate_config(config):
            raise ValueError("Invalid config format")
        
        self._configs[format_name] = config
    
    def save_config(self, format_name: str, config_path: str = None):
        """
        保存配置到文件
        
        Args:
            format_name: 格式名称
            config_path: 保存路径，如果为None则保存到默认位置
        """
        if format_name not in self._configs:
            raise KeyError(f"Format '{format_name}' not found")
        
        if config_path is None:
            config_path = os.path.join(self.config_dir, f"{format_name}.yaml")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self._configs[format_name], f, default_flow_style=False, allow_unicode=True)
