# Configuration-Driven Dataset Translation Tool / 配置驱动的数据集翻译工具

[English](#english) | [中文](#中文)

---

## English

A universal dataset translation tool that supports multiple data formats through configuration files. Easily translate datasets of any format with YAML configuration files.

### 🚀 Features

- ✅ **Configuration-Driven Format Support**: Define data formats through YAML configuration files
- ✅ **Multiple Pre-built Formats**: Built-in support for Alpaca, ShareGPT, OpenAI and other common formats
- ✅ **Custom Format Support**: Easily add new data format configurations
- ✅ **Automatic Format Detection**: Intelligent recognition of dataset formats
- ✅ **Flexible Field Mapping**: Support for simple fields and complex nested structures
- ✅ **Conditional Translation Filtering**: Support for selective translation based on conditions

### 🛠️ Installation

```bash

# use conda environment
conda env create -f environment.yml
```

### ⚙️ Environment Setup

1. Create a `.env` file and configure:

```env
MODEL=deepseek-chat
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com
```

### 🎯 Usage

#### 1. List All Available Formats

```bash
python translate_dataset.py --list_formats
```

#### 2. Translate Using Pre-built Formats

**Alpaca Format Translation:**

```bash
python translate_dataset.py \
  --dataset samhog/psychology-10k \
  --format alpaca \
  --from_lang en \
  --to_lang zh-CN \
  --output datasets/psychology-10k-zh
```

**ShareGPT Format Translation:**

```bash
python translate_dataset.py \
  --dataset your/sharegpt-dataset \
  --format sharegpt \
  --from_lang en \
  --to_lang zh-CN
```

#### 3. Translate Using Custom Formats

**Custom Reasoning Dataset:**

```bash
python translate_dataset.py \
  --dataset your/reasoning-dataset \
  --format custom_reasoning \
  --from_lang en \
  --to_lang zh-CN
```

#### 4. Automatic Format Detection

```bash
python translate_dataset.py \
  --dataset your/dataset \
  --auto_detect \
  --from_lang en \
  --to_lang zh-CN
```

### 📝 Supported Data Formats

#### 1. Alpaca Format

```yaml
translatable_fields:
  - instruction (required)
  - input (optional)
  - output (required)
```

#### 2. ShareGPT Format

```yaml
translatable_fields:
  - conversations (list)
    - value (condition: from=human|gpt|assistant)
```

#### 3. OpenAI Format

```yaml
translatable_fields:
  - messages (list)
    - content (condition: role=user|assistant|system)
```

#### 4. Custom Reasoning Format

```yaml
translatable_fields:
  - statement (required)
  - reasoning (required)
  - classification (required)
  - pure_observation_alternative (optional)
```

### 🔧 Custom Format Configuration

To support new data formats, simply create a new YAML file in the `configs/` directory:

```yaml
name: "your_format"
description: "Your custom format description"
translatable_fields:
  - field: "field_name"
    type: "string" # string or list
    required: true # whether required
    description: "Field description"
  - field: "list_field"
    type: "list"
    sub_fields:
      - field: "sub_field"
        type: "string"
        condition: "role:user|assistant" # condition filtering
```

#### Supported Field Types:

1. **string**: Simple string fields
2. **list**: List fields, require sub_fields configuration
3. **Conditional filtering**: Use condition parameter to filter specific values

### 🧪 Testing Configuration System

Run the test script to verify configuration and format processors:

```bash
python test_config.py
```

### 📚 Usage Examples

View detailed usage examples:

```bash
python example_usage.py
```

---

## 中文

一个支持多种数据格式的通用数据集翻译工具，通过配置文件驱动实现对任意格式数据集的翻译支持。

### 🚀 功能特点

- ✅ **配置驱动的格式支持**：通过 YAML 配置文件定义数据格式
- ✅ **多种预设格式**：内置支持 Alpaca、ShareGPT、OpenAI 等常见格式
- ✅ **自定义格式支持**：轻松添加新的数据格式配置
- ✅ **自动格式检测**：智能识别数据集格式
- ✅ **灵活的字段映射**：支持简单字段和复杂嵌套结构
- ✅ **条件过滤翻译**：支持基于条件的选择性翻译

### 🛠️ 安装依赖

```bash

# 安装conda
# 使用conda环境
conda env create -f environment.yml
```

### ⚙️ 环境配置

1. 创建 `.env` 文件并配置：

```env
MODEL=deepseek-chat
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com
```

### 🎯 使用方法

#### 1. 查看所有可用格式

```bash
python translate_dataset.py --list_formats
```

#### 2. 使用预设格式翻译

**Alpaca 格式翻译：**

```bash
python translate_dataset.py \
  --dataset samhog/psychology-10k \
  --format alpaca \
  --from_lang en \
  --to_lang zh-CN \
  --output datasets/psychology-10k-zh
```

**ShareGPT 格式翻译：**

```bash
python translate_dataset.py \
  --dataset your/sharegpt-dataset \
  --format sharegpt \
  --from_lang en \
  --to_lang zh-CN
```

#### 3. 使用自定义格式翻译

**自定义 reasoning 数据集：**

```bash
python translate_dataset.py \
  --dataset your/reasoning-dataset \
  --format custom_reasoning \
  --from_lang en \
  --to_lang zh-CN
```

#### 4. 自动检测格式

```bash
python translate_dataset.py \
  --dataset your/dataset \
  --auto_detect \
  --from_lang en \
  --to_lang zh-CN
```

### 📝 支持的数据格式

#### 1. Alpaca 格式

```yaml
translatable_fields:
  - instruction (必需)
  - input (可选)
  - output (必需)
```

#### 2. ShareGPT 格式

```yaml
translatable_fields:
  - conversations (list)
    - value (条件: from=human|gpt|assistant)
```

#### 3. OpenAI 格式

```yaml
translatable_fields:
  - messages (list)
    - content (条件: role=user|assistant|system)
```

#### 4. 自定义 reasoning 格式

```yaml
translatable_fields:
  - statement (必需)
  - reasoning (必需)
  - classification (必需)
  - pure_observation_alternative (可选)
```

### 🔧 自定义格式配置

要支持新的数据格式，只需在 `configs/` 目录下创建新的 YAML 文件：

```yaml
name: "your_format"
description: "Your custom format description"
translatable_fields:
  - field: "field_name"
    type: "string" # string 或 list
    required: true # 是否必需
    description: "字段说明"
  - field: "list_field"
    type: "list"
    sub_fields:
      - field: "sub_field"
        type: "string"
        condition: "role:user|assistant" # 条件过滤
```

#### 支持的字段类型：

1. **string**: 简单字符串字段
2. **list**: 列表字段，需要配置 sub_fields
3. **条件过滤**: 使用 condition 参数过滤特定值

### 🧪 测试配置系统

运行测试脚本验证配置和格式处理器：

```bash
python test_config.py
```

### 📚 使用示例

查看详细使用示例：

```bash
python example_usage.py
```
