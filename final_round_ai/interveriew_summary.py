import requests

# 1. 加载环境变量（API密钥存储在.env文件中）
API_KEY = "xxxxxxxxxxxxx"


# 2. 定义DeepSeek API调用函数
def analyze_text_with_deepseek(text):
    """
    使用DeepSeek API分析并总结文本
    :param text: 需要分析的文本内容
    :return: DeepSeek生成的总结内容
    """
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 构造提示词（可调整优化）
    prompt = f"""请对以下软件开发的面试对话进行总结，要求：
    1. 总结被面试者的优点，缺点，擅长的技能
    2. 以时间线的形式输出
    3. 保持客观准确
    4. 请用纯html格式回答，方便后续保存为html文件
    文本内容：
    {text}"""

    data = {
        "model": "deepseek-chat",  # 或其他可用模型
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,  # 控制创造性（0-2）
        "max_tokens": 1000  # 限制响应长度
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # 检查HTTP错误
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"API调用失败: {str(e)}")
        return None


# 3. 测试调用
if __name__ == "__main__":
    sample_text = """[09:00:23] 面试官：李同学你好，欢迎参加今天的面试。我们直接从技术开始。请先简要介绍一下Transformer架构的核心机制，并说明它在现代大语言模型（如GPT）中的作用。

[09:01:10] 面试者：王经理您好。Transformer的核心是“自注意力机制”（Self-Attention），它允许模型在处理一个词时，直接关注并加权计算输入序列中所有其他词的重要性，从而高效地捕捉长距离上下文依赖。在GPT这类模型中，它被用作解码器，通过多层堆叠和掩码机制，实现从左到右的自回归生成，即逐个预测下一个 token。

[09:02:55] 面试官：解释得很清晰。那么，请再谈谈RAG（检索增强生成）的工作流程和它要解决的核心问题。

[09:03:40] 面试者：好的。RAG主要用于解决大模型的事实性幻觉和知识滞后问题。它的工作流程分为两步：第一步是“检索”，根据用户问题，从一个庞大的外部知识库（如向量数据库）中检索出最相关的文档片段；第二步是“生成”，将检索到的片段与原始问题一并作为上下文，输入给大语言模型，从而生成一个信息更准确、更可靠的回答。

[09:05:15] 面试官：如果让你来优化一个RAG系统的检索环节效率，你会优先考虑哪些技术方向？

[09:05:50] 面试者：我会从几个方面入手：第一，采用混合检索（Hybrid Search），结合基于关键词的BM25算法和基于语义的向量相似度检索，取长补短。第二，为向量索引使用更高效的算法，比如HNSW（分层可导航小世界图），来加速最近邻搜索。第三，引入缓存机制，对高频或相似的查询结果进行缓存，避免重复的检索计算。"""

    summary = analyze_text_with_deepseek(sample_text)
    print("DeepSeek分析结果：")
    print(summary)

    with open("summary.html", "w", encoding="utf-8") as file:
        file.write(summary)