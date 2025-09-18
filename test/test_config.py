#!/usr/bin/env python3
"""
测试配置系统的功能
"""

from packages.config import ConfigManager
from packages.formats.generic import GenericFormatHandler

def test_config_loading():
    """测试配置加载功能"""
    print("=== 测试配置加载 ===")
    
    try:
        config_manager = ConfigManager("configs")
        formats = config_manager.list_formats()
        print(f"已加载的格式: {formats}")
        
        for format_name in formats:
            config = config_manager.get_config(format_name)
            print(f"\n格式: {format_name}")
            print(f"描述: {config.get('description', 'No description')}")
            print(f"可翻译字段:")
            for field in config['translatable_fields']:
                print(f"  - {field['field']} ({field.get('type', 'string')})")
                if field.get('required'):
                    print(f"    [必需字段]")
        
        return True
    except Exception as e:
        print(f"配置加载失败: {str(e)}")
        return False

def test_format_handler():
    """测试格式处理器功能"""
    print("\n=== 测试格式处理器 ===")
    
    try:
        config_manager = ConfigManager("configs")
        
        # 测试您的自定义格式
        handler = config_manager.create_format_handler("custom_reasoning")
        print(f"创建处理器: {handler.name}")
        
        # 模拟您的数据格式
        sample_data = {
            "statement": "This is a test statement to analyze.",
            "reasoning": "The reasoning behind this analysis is based on logical principles.",
            "classification": "Test Classification",
            "pure_observation_alternative": "Alternative observation for this case."
        }
        
        print(f"\n测试数据: {sample_data}")
        
        # 验证格式
        is_valid = handler.validate_item(sample_data)
        print(f"格式验证: {'通过' if is_valid else '失败'}")
        
        # 提取可翻译内容
        translatable_fields = handler.extract_translatable_content(sample_data)
        print(f"\n提取到 {len(translatable_fields)} 个可翻译字段:")
        for field in translatable_fields:
            print(f"  {field.field_path}: {field.content[:50]}...")
        
        # 模拟翻译后重新组装
        for field in translatable_fields:
            field.content = f"[翻译] {field.content}"
        
        reconstructed = handler.reconstruct_item(sample_data, translatable_fields)
        print(f"\n重新组装后的数据:")
        for key, value in reconstructed.items():
            print(f"  {key}: {value[:50]}..." if len(str(value)) > 50 else f"  {key}: {value}")
        
        return True
    except Exception as e:
        print(f"格式处理器测试失败: {str(e)}")
        return False

def test_auto_detection():
    """测试自动格式检测"""
    print("\n=== 测试自动格式检测 ===")
    
    try:
        config_manager = ConfigManager("configs")
        
        # 测试不同格式的样本数据
        test_samples = {
            "alpaca": {
                "instruction": "Translate the following text",
                "input": "Hello world",
                "output": "你好世界"
            },
            "custom_reasoning": {
                "statement": "Test statement",
                "reasoning": "Test reasoning",
                "classification": "Test class",
                "pure_observation_alternative": "Alternative"
            },
            "unknown": {
                "some_field": "some_value",
                "another_field": "another_value"
            }
        }
        
        for sample_name, sample_data in test_samples.items():
            detected = config_manager.detect_format(sample_data)
            print(f"样本 '{sample_name}' 检测结果: {detected}")
        
        return True
    except Exception as e:
        print(f"自动检测测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始测试配置驱动的翻译系统...")
    
    success = True
    success &= test_config_loading()
    success &= test_format_handler()
    success &= test_auto_detection()
    
    print(f"\n测试结果: {'全部通过' if success else '部分失败'}")
