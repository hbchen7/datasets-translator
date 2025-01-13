import json
import os
import asyncio
from typing import List, Dict
from datasets import load_dataset
from packages.openai import OpenAIHandler
from packages.translate import OpenAITranslator

# 可配置的翻译字段
TRANSLATE_FIELDS = ["input", "output"]

async def translate_alpaca_dataset(
    dataset_path: str,
    from_lang: str = "en",
    to_lang: str = "zh-CN",
    output_path: str = None,
    max_concurrent: int = 200
):
    """
    翻译数据集
    
    Args:
        dataset_path: 数据集路径或名称
        from_lang: 源语言代码，默认en
        to_lang: 目标语言代码，默认zh-CN
        output_path: 输出路径，默认与输入路径相同
        openai_url: OpenAI API地址
        openai_key: OpenAI API密钥
        max_concurrent: 最大并发数，默认200
    """
    # 从环境变量获取OpenAI配置
    openai_url = os.getenv("OPENAI_BASE_URL")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_url or not openai_key:
        raise EnvironmentError("Please set OPENAI_BASE_URL and OPENAI_API_KEY in environment variables")
    # 初始化OpenAI处理器和翻译器
    openai_handler = OpenAIHandler(
        model="deepseek-chat",
        openai_url=openai_url or os.getenv("OPENAI_BASE_URL"),
        openai_key=openai_key or os.getenv("OPENAI_API_KEY")
    )
    translator = OpenAITranslator(openai_handler)

    # 加载数据集
    dataset = load_dataset(dataset_path)
    
    # 创建信号量控制并发
    semaphore = asyncio.Semaphore(max_concurrent)

    async def translate_item(item: Dict) -> Dict:
        """
        翻译单个数据项
        """
        async with semaphore:
            # print("translate item", item)
            # 只翻译指定字段
            for field in TRANSLATE_FIELDS:
                if field in item:
                    try:
                        item[field] = await translator.translate(
                            from_lang=from_lang,
                            to_lang=to_lang,
                            text=item[field]
                        )
                    except Exception as e:
                        print(f"Error translating {field}: {str(e)}")
                        continue
            return item

    # 处理所有split
    translated_splits = {}
    for split_name, split_data in dataset.items():
        print(f"Translating split: {split_name}")
        
        # 并发翻译
        # tasks = [translate_item(item) for item in split_data.select(range(20))]  # 使用select方法选取前20条数据进行翻译
        # 使用select方法选取数据，避免一次性加载全部数据
        tasks = [translate_item(item) for item in split_data.select(range(len(split_data)))]
        translated_items = await asyncio.gather(*tasks)
        
        translated_splits[split_name] = translated_items

    # 保存翻译后的数据集
    output_path = output_path or dataset_path
    dataset.save_to_disk(output_path)
    # 保存一份JSON格式的副本
    json_path = os.path.join(output_path, "full.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(translated_splits, f, ensure_ascii=False, indent=2)
    print(f"Translated dataset JSON saved to: {json_path}")
    print(f"Translated dataset saved to: {output_path}")

if __name__ == "__main__":
    import argparse
    import os
    from dotenv import load_dotenv
    load_dotenv()  # 加载.env文件中的环境变量
    
    # 创建参数解析器
    # python alpaca.py --dataset=samhog/psychology-10k --from_lang=en --to_lang=zh-CN --output=datasets/psychology-10k-zh
    parser = argparse.ArgumentParser(description="数据集翻译脚本")
    parser.add_argument("--dataset", required=True, help="数据集路径或名称")
    parser.add_argument("--from_lang", required=True, help="源语言代码")
    parser.add_argument("--to_lang", required=True, help="目标语言代码")
    parser.add_argument("--output", help="输出路径，默认为输入路径")
    
    # 解析参数
    args = parser.parse_args()
    
    # 运行翻译任务
    asyncio.run(translate_alpaca_dataset(
        dataset_path=args.dataset,
        from_lang=args.from_lang,
        to_lang=args.to_lang,
        output_path=args.output,
    ))
