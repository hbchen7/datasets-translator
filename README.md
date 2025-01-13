# 数据集翻译工具

本项目是一个用于翻译数据集的工具（目前仅支持 alpaca 格式），目前支持通过命令行脚本调用进行数据集翻译。

## 功能特点
- 支持alpaca格式数据集翻译
- 支持多语言翻译（需配置翻译模型）
- 支持并发翻译，提高翻译效率
- 自动保存翻译结果到指定路径
- 生成JSON格式的翻译结果文件

## 已转换数据集

| 原始数据集 | 翻译后数据集 | 备注 |
|-----------|-------------|------|
| [samhog/psychology-10k](https://huggingface.co/datasets/samhog/psychology-10k) | [wangerzi/psychology-10k-zh](https://huggingface.co/datasets/wj2015/psychology-10k-zh) | 翻译为中文心理学领域数据集 |


## 环境配置

### 使用conda创建虚拟环境

1. 确保已安装conda
2. 在项目根目录下运行以下命令创建虚拟环境：

## 环境
初始化环境
```bash
conda env create -f environment.yml
```

持久化环境
```bash
conda env export --no-builds > environment.yml
```

## 配置说明

1. 将 `.env.template` 文件重命名为 `.env`
2. 在 `.env` 文件中配置 OpenAI API 信息：
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_BASE_URL=https://api.deepseek.com
   ```

## 使用说明

### 翻译数据集

运行以下命令进行数据集翻译：

```bash
python alpaca.py --dataset=samhog/psychology-10k --from_lang=en --to_lang=zh-CN --output=datasets/psychology-10k-zh
```
