import streamlit as st
from datasets import load_dataset  # 加载数据集
import json  # 用于JSON格式化

def show_dataset():
    # 设置页面标题
    st.title("数据集展示")
    
    # 创建输入框获取数据集名称
    dataset_name = st.text_input("请输入数据集名称（例如：samhog/psychology-10k）", 
                               value="samhog/psychology-10k")
    
    try:
        # 加载数据集
        dataset = load_dataset(dataset_name)
        
        # 显示数据集信息
        st.write(f"数据集包含 {len(dataset)} 个 split")
        
        # 选择要查看的split
        split_names = list(dataset.keys())
        selected_split = st.selectbox("请选择要查看的split", split_names)
        
        # 获取选中的split数据
        split_data = dataset[selected_split]
        st.write(f"当前split大小：{len(split_data)} 条记录")
        st.write(f"数据集列名：{split_data.column_names}")
        
        # 分批次读取设置
        batch_size = st.slider("选择每批显示的数据量", 100, 5000, 1000, 100)
        total_batches = (len(split_data) + batch_size - 1) // batch_size
        
        # 添加批次选择器
        batch_num = st.number_input(f"选择要查看的批次 (共 {total_batches} 批)", 
                                  min_value=1, 
                                  max_value=total_batches, 
                                  value=1)
        
        # 计算当前批次的起止位置
        start_idx = (batch_num - 1) * batch_size
        end_idx = min(start_idx + batch_size, len(split_data))
        
        # 获取当前批次数据
        batch_data = split_data.select(range(start_idx, end_idx))
        
        # 将批次数据转换为pandas DataFrame格式
        df = batch_data.to_pandas()
        
        if 'conversations' in df.columns:
            # 处理ndarray类型数据
            df['conversations'] = df['conversations'].apply(
                lambda x: json.dumps(x.tolist() if hasattr(x, 'tolist') else x, 
                                   ensure_ascii=False, 
                                   indent=2)
            )
        
        # 展示当前批次数据
        st.write(f"正在显示 {selected_split} split 的第 {batch_num} 批数据 ({start_idx + 1}-{end_idx} 条):")
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"加载数据集失败: {str(e)}")

if __name__ == "__main__":
    show_dataset()
