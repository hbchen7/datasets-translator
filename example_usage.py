#!/usr/bin/env python3
"""
新的配置驱动翻译系统使用示例
"""

import os
from dotenv import load_dotenv

def show_usage_examples():
    """显示使用示例"""
    
    print("=== 配置驱动的数据集翻译系统 ===\n")
    
    print("1. 查看所有可用格式:")
    print("   python translate_dataset.py --list_formats\n")
    
    print("2. 使用预设的alpaca格式翻译:")
    print("   python translate_dataset.py \\")
    print("     --dataset samhog/psychology-10k \\")
    print("     --format alpaca \\")
    print("     --from_lang en \\")
    print("     --to_lang zh-CN \\")
    print("     --output datasets/psychology-10k-zh\n")
    
    print("3. 使用您的自定义reasoning格式:")
    print("   python translate_dataset.py \\")
    print("     --dataset your/reasoning-dataset \\")
    print("     --format custom_reasoning \\")
    print("     --from_lang en \\")
    print("     --to_lang zh-CN\n")
    
    print("4. 自动检测格式:")
    print("   python translate_dataset.py \\")
    print("     --dataset your/dataset \\")
    print("     --auto_detect \\")
    print("     --from_lang en \\")
    print("     --to_lang zh-CN\n")
    
    print("5. ShareGPT格式翻译:")
    print("   python translate_dataset.py \\")
    print("     --dataset your/sharegpt-dataset \\")
    print("     --format sharegpt \\")
    print("     --from_lang en \\")
    print("     --to_lang zh-CN\n")
    
    print("=== 配置文件结构说明 ===\n")
    
    print("您的自定义格式配置文件 (configs/custom_reasoning.yaml):")
    print("""
name: "custom_reasoning"
description: "Custom format for reasoning dataset"
translatable_fields:
  - field: "statement"
    type: "string"
    required: true
  - field: "reasoning"
    type: "string"
    required: true
  - field: "classification"
    type: "string"
    required: true
  - field: "pure_observation_alternative"
    type: "string"
    required: false
""")
    
    print("\n=== 支持的字段类型 ===\n")
    print("1. string: 简单字符串字段")
    print("2. list: 列表字段，需要配置sub_fields")
    print("3. 条件过滤: 使用condition参数过滤特定值")
    
    print("\n=== 扩展到其他格式 ===\n")
    print("要支持新格式，只需创建新的YAML配置文件：")
    print("1. 在configs/目录下创建新的.yaml文件")
    print("2. 定义name, description和translatable_fields")
    print("3. 重新运行翻译脚本即可自动加载新格式")

def create_sample_config():
    """创建一个示例配置文件"""
    sample_config = """name: "example_format"
description: "Example format for demonstration"
translatable_fields:
  - field: "title"
    type: "string"
    required: true
    description: "Document title"
  - field: "content"
    type: "string"
    required: true
    description: "Main content"
  - field: "summary"
    type: "string"
    required: false
    description: "Optional summary"
  - field: "tags"
    type: "list"
    required: false
    description: "List of tag strings"
"""
    
    with open("configs/example_format.yaml", "w", encoding="utf-8") as f:
        f.write(sample_config)
    
    print("创建了示例配置文件: configs/example_format.yaml")
    print("您可以参考这个文件创建自己的格式配置")

if __name__ == "__main__":
    load_dotenv()
    
    show_usage_examples()
    
    print("\n" + "="*50)
    create_sample_config()
    
    print("\n" + "="*50)
    print("Ready to use! 系统已准备就绪！")
    print("请确保设置了环境变量 OPENAI_BASE_URL 和 OPENAI_API_KEY")
