import json
import os
import asyncio
from typing import List, Dict, Optional
from datasets import load_dataset
from packages.openai import OpenAIHandler
from packages.translate import OpenAITranslator
from packages.config import ConfigManager
from packages.formats.base import TranslatableField

async def translate_dataset(
    dataset_path: str,
    format_name: str,
    from_lang: str = "en",
    to_lang: str = "zh-CN",
    output_path: str = None,
    max_concurrent: int = 5,
    config_dir: str = "configs"
):
    """
    通用数据集翻译函数
    
    Args:
        dataset_path: 数据集路径或名称
        format_name: 数据格式名称（如 alpaca, sharegpt, custom_reasoning）
        from_lang: 源语言代码，默认en
        to_lang: 目标语言代码，默认zh-CN
        output_path: 输出路径，默认与输入路径相同
        max_concurrent: 最大并发数，默认200
        config_dir: 配置文件目录，默认configs
    """
    # 从环境变量获取OpenAI配置
    openai_url = os.getenv("OPENAI_BASE_URL")
    openai_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL")
    if not openai_url or not openai_key or not model_name:
        raise EnvironmentError("Please set OPENAI_BASE_URL, OPENAI_API_KEY, and MODEL in environment variables")
    
    # 初始化配置管理器和格式处理器
    config_manager = ConfigManager(config_dir)
    print(f"Available formats: {config_manager.list_formats()}")
    
    # 创建格式处理器
    format_handler = config_manager.create_format_handler(format_name)
    print(f"Using format: {format_handler.name} - {format_handler.description}")
    
    # 初始化OpenAI处理器和翻译器
    openai_handler = OpenAIHandler(
        model=model_name,
        openai_url=openai_url,
        openai_key=openai_key
    )
    translator = OpenAITranslator(openai_handler)

    # 加载数据集
    print(f"Loading dataset: {dataset_path}")
    dataset = load_dataset(dataset_path)
    
    # 创建信号量控制并发
    semaphore = asyncio.Semaphore(max_concurrent)

    async def translate_item(item: Dict) -> Dict:
        """翻译单个数据项"""
        async with semaphore:
            try:
                # 提取可翻译内容
                translatable_fields = format_handler.extract_translatable_content(item)
                
                if not translatable_fields:
                    print(f"No translatable content found in item: {item}")
                    return item
                
                # 翻译所有字段
                for field in translatable_fields:
                    if field.content and isinstance(field.content, str):
                        try:
                            translated_content = await translator.translate(
                                from_lang=from_lang,
                                to_lang=to_lang,
                                text=field.content
                            )
                            field.content = translated_content
                        except Exception as e:
                            print(f"Error translating field {field.field_path}: {str(e)}")
                            continue
                
                # 重新组装数据项
                translated_item = format_handler.reconstruct_item(item, translatable_fields)
                return translated_item
                
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                return item

    # 处理所有split
    translated_splits = {}
    for split_name, split_data in dataset.items():
        print(f"Translating split: {split_name} ({len(split_data)} items)")
        
        # 验证数据格式
        if len(split_data) > 0:
            sample_item = split_data[0]
            if not format_handler.validate_item(sample_item):
                print(f"Warning: Sample item may not match expected format")
                print(f"Sample item keys: {list(sample_item.keys())}")
                print(f"Expected fields: {[field['field'] for field in format_handler.translatable_fields]}")
        
        # 并发翻译
        tasks = [translate_item(item) for item in split_data.select(range(len(split_data)))]
        translated_items = await asyncio.gather(*tasks)
        
        translated_splits[split_name] = translated_items

    # 保存翻译后的数据集
    output_path = output_path or f"{dataset_path}_translated"
    
    # 创建输出目录
    os.makedirs(output_path, exist_ok=True)
    
    # 保存JSON格式的翻译结果
    json_path = os.path.join(output_path, "translated_dataset.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(translated_splits, f, ensure_ascii=False, indent=2)
    
    print(f"Translated dataset JSON saved to: {json_path}")
    print(f"Translation completed successfully!")
    
    # 显示统计信息
    total_items = sum(len(split_data) for split_data in translated_splits.values())
    print(f"Total items translated: {total_items}")
    print(f"Splits processed: {list(translated_splits.keys())}")

def auto_detect_format(dataset_path: str, config_dir: str = "configs") -> Optional[str]:
    """
    自动检测数据集格式
    
    Args:
        dataset_path: 数据集路径
        config_dir: 配置目录
        
    Returns:
        Optional[str]: 检测到的格式名称
    """
    try:
        dataset = load_dataset(dataset_path)
        config_manager = ConfigManager(config_dir)
        
        # 获取第一个split的第一个样本
        first_split = next(iter(dataset.values()))
        if len(first_split) > 0:
            sample_item = first_split[0]
            detected_format = config_manager.detect_format(sample_item)
            
            if detected_format:
                print(f"Auto-detected format: {detected_format}")
                return detected_format
            else:
                print("Could not auto-detect format. Available formats:")
                for fmt in config_manager.list_formats():
                    config = config_manager.get_config(fmt)
                    fields = [field['field'] for field in config['translatable_fields']]
                    print(f"  {fmt}: {fields}")
                return None
        
    except Exception as e:
        print(f"Error during auto-detection: {str(e)}")
        return None

if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv
    load_dotenv()  # 加载.env文件中的环境变量
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="通用数据集翻译脚本")
    parser.add_argument("--dataset", required=True, help="数据集路径或名称")
    parser.add_argument("--format", help="数据格式名称（如 alpaca, sharegpt, custom_reasoning）")
    parser.add_argument("--from_lang", required=True, help="源语言代码")
    parser.add_argument("--to_lang", required=True, help="目标语言代码")
    parser.add_argument("--output", help="输出路径，默认为数据集名_translated")
    parser.add_argument("--config_dir", default="configs", help="配置文件目录")
    parser.add_argument("--auto_detect", action="store_true", help="自动检测数据格式")
    parser.add_argument("--list_formats", action="store_true", help="列出所有可用格式")
    
    # 解析参数
    args = parser.parse_args()
    
    # 如果要求列出格式，则显示并退出
    if args.list_formats:
        config_manager = ConfigManager(args.config_dir)
        print("Available formats:")
        for fmt in config_manager.list_formats():
            config = config_manager.get_config(fmt)
            print(f"  {fmt}: {config.get('description', 'No description')}")
            fields = [field['field'] for field in config['translatable_fields']]
            print(f"    Fields: {fields}")
        exit(0)
    
    # 确定要使用的格式
    format_name = args.format
    
    if args.auto_detect or not format_name:
        print("Attempting to auto-detect format...")
        detected_format = auto_detect_format(args.dataset, args.config_dir)
        if detected_format:
            format_name = detected_format
        elif not format_name:
            print("Please specify --format parameter")
            exit(1)
    
    if not format_name:
        print("No format specified. Use --format or --auto_detect")
        exit(1)
    
    print(f"Using format: {format_name}")
    
    # 运行翻译任务
    asyncio.run(translate_dataset(
        dataset_path=args.dataset,
        format_name=format_name,
        from_lang=args.from_lang,
        to_lang=args.to_lang,
        output_path=args.output,
        config_dir=args.config_dir
    ))
