from typing import List
from .openai import OpenAIHandler

# 其他经过验证的代码都可以，视模型支持情况而定
from_languages = [
    {"name": "中文", "code": "zh-CN"},
    {"name": "英语", "code": "en"},
    {"name": "日语", "code": "ja"},
    {"name": "法语", "code": "fr"},
    {"name": "德语", "code": "de"},
]
to_languages = from_languages[1:] + [from_languages[0]]

class OpenAITranslator:
    def __init__(self, openai_handler: OpenAIHandler):
        self.openai_handler = openai_handler

    async def translate(self, from_lang: str, to_lang: str, text: str) -> str:
        if from_lang == to_lang:
            raise ValueError("Source and target languages cannot be the same")
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        sysprompt = (
            f"你是一位专业的翻译专家，擅长在不同语言之间进行翻译，特别是{from_lang}和{to_lang}之间的翻译。\n\n"
            f"任务：提供准确的{from_lang}到{to_lang}的翻译。\n"
            f"范围：专注于保持原文的含义和上下文。\n"
            f"语气：使用正式和专业的语气。\n"
            f"注意：确保{to_lang}的翻译结果中不包含任何{from_lang}的字符或单词。\n\n"
        )

        messages = [
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": text}
        ]

        translated_text = await self.openai_handler.request(
            messages=messages,
            temp=0.7
        )

        return translated_text
