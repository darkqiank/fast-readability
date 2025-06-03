# Fast Readability

一个基于 Mozilla Readability.js 的快速 HTML 内容提取器，用于从网页中提取干净的文章内容。

## 特性

- 🚀 **快速**: 基于 JavaScript 引擎的高性能内容提取
- 🧹 **干净**: 自动移除广告、导航栏、侧边栏等无关内容
- 🌐 **多语言**: 支持多种语言的网页内容提取
- 📱 **易用**: 简单的 Python API，支持 HTML 字符串和 URL
- 🔧 **可配置**: 支持自定义请求头、超时等参数

## 安装

```bash
pip install fast-readability
```

或者从源码安装：

```bash
git clone https://github.com/jiankaiwang/fast-readability.git
cd fast-readability
pip install -e .
```

## 快速开始

### 从 URL 提取内容

```python
from fast_readability import Readability

# 创建提取器实例
reader = Readability()

# 从 URL 提取内容
url = "https://example.com/article"
result = reader.extract_from_url(url)

print("标题:", result["title"])
print("正文:", result["textContent"])
print("HTML内容:", result["content"])
```

### 从 HTML 字符串提取内容

```python
from fast_readability import Readability

# HTML 内容
html = """
<html>
<head><title>示例文章</title></head>
<body>
    <article>
        <h1>这是标题</h1>
        <p>这是文章的正文内容...</p>
    </article>
    <aside>这是侧边栏，会被过滤掉</aside>
</body>
</html>
"""

reader = Readability()
result = reader.extract_from_html(html)

print("标题:", result["title"])
print("正文:", result["textContent"])
```

### 便捷函数

```python
from fast_readability import extract_content, extract_from_url

# 直接从 HTML 提取
result = extract_content(html)

# 直接从 URL 提取
result = extract_from_url("https://example.com/article")
```

## API 参考

### Readability 类

#### `__init__(debug=False)`

创建 Readability 实例。

- `debug` (bool): 是否启用调试模式

#### `extract_from_html(html)`

从 HTML 字符串提取内容。

- `html` (str): HTML 字符串

返回包含以下字段的字典：
- `title`: 文章标题
- `content`: HTML 格式的文章内容
- `textContent`: 纯文本格式的文章内容
- `length`: 内容长度
- `excerpt`: 文章摘要
- `byline`: 作者信息
- `dir`: 文本方向
- `siteName`: 网站名称
- `lang`: 语言

#### `extract_from_url(url, headers=None, timeout=30, verify_ssl=True)`

从 URL 提取内容。

- `url` (str): 要提取的 URL
- `headers` (dict, optional): 自定义请求头
- `timeout` (int): 请求超时时间（秒）
- `verify_ssl` (bool): 是否验证 SSL 证书

#### `get_text_content(html)`

获取纯文本内容。

#### `get_title(html)`

获取文章标题。

#### `is_probably_readable(html, min_content_length=140)`

检查 HTML 是否包含可读内容。

### 便捷函数

#### `extract_content(html, debug=False)`

从 HTML 提取内容的便捷函数。

#### `extract_from_url(url, debug=False, **kwargs)`

从 URL 提取内容的便捷函数。

## 使用示例

### 处理不同类型的网站

```python
from fast_readability import Readability

reader = Readability(debug=True)

# 新闻网站
news_result = reader.extract_from_url("https://news.example.com/article")

# 博客文章
blog_result = reader.extract_from_url("https://blog.example.com/post")

# 技术文档
doc_result = reader.extract_from_url("https://docs.example.com/guide")
```

### 自定义请求参数

```python
from fast_readability import Readability

reader = Readability()

# 自定义请求头
headers = {
    'User-Agent': 'MyBot/1.0',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

result = reader.extract_from_url(
    "https://example.com/article",
    headers=headers,
    timeout=60,
    verify_ssl=False
)
```

### 批量处理

```python
from fast_readability import Readability

urls = [
    "https://example1.com/article",
    "https://example2.com/article",
    "https://example3.com/article"
]

reader = Readability()

for url in urls:
    try:
        result = reader.extract_from_url(url)
        print(f"Title: {result['title']}")
        print(f"Length: {result['length']} chars")
        print("-" * 50)
    except Exception as e:
        print(f"Failed to extract {url}: {e}")
```

## 依赖项

- Python 3.7+
- quickjs
- beautifulsoup4
- requests
- urllib3

## 许可证

本项目基于 Mozilla Public License 2.0 许可证。

## 贡献

欢迎提交 Issues 和 Pull Requests！

## 致谢

本项目基于以下开源项目：
- [Mozilla Readability.js](https://github.com/mozilla/readability) - 核心内容提取算法
- [JSDOMParser](https://github.com/mozilla/readability/blob/main/JSDOMParser.js) - JavaScript DOM 解析器 