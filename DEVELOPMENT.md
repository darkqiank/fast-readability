# Fast-Readability Development Guide

## 项目架构

Fast-Readability 是一个使用 QuickJS 调用 Mozilla readability.js 的 Python 库，提供了完整的文章内容提取功能。

### 核心组件

#### 1. `fast_readability/readability.py`
- **`Readability`** 类：主要的核心类
- **`ReadabilityResult`** 数据类：存储解析结果
- **`ReadabilityError`** 异常类：自定义错误类型

#### 2. `fast_readability/utils.py`
- 工具函数模块，提供便捷的API
- `parse_html()`: 快速解析HTML
- `is_probably_readerable()`: 检查内容是否可读
- `create_custom_options()`: 创建自定义选项

#### 3. `fast_readability/cli.py`
- 命令行界面工具
- 支持多种输入输出格式
- 完整的参数配置

#### 4. JavaScript 文件 (`fast_readability/js/`)
- `JSDOMParser.js`: Mozilla的DOM解析器
- `Readability.js`: Mozilla的可读性算法
- `readability_wrapper.js`: 自定义的包装器，提供Python接口

### 技术栈

- **Python 3.7+**: 主要编程语言
- **QuickJS**: JavaScript执行引擎
- **Mozilla Readability.js**: 核心算法
- **Requests**: HTTP客户端（可选）

## 开发设置

### 环境要求

```bash
# 基本依赖
pip install quickjs requests

# 开发依赖
pip install pytest pytest-cov black isort flake8 mypy build
```

### 项目结构

```
fast-readability/
├── fast_readability/           # 主要源代码
│   ├── __init__.py            # 包初始化
│   ├── readability.py         # 核心功能
│   ├── utils.py               # 工具函数
│   ├── cli.py                 # 命令行工具
│   └── js/                    # JavaScript文件
│       ├── JSDOMParser.js     # DOM解析器
│       ├── Readability.js     # 可读性算法
│       └── readability_wrapper.js  # Python接口包装器
├── tests/                     # 测试文件
│   ├── test_readability.py    # 核心功能测试
│   └── test_utils.py          # 工具函数测试
├── examples/                  # 使用示例
│   └── basic_usage.py         # 基本用法示例
├── pyproject.toml             # 项目配置
├── README.md                  # 项目文档
├── LICENSE                    # 许可证
└── DEVELOPMENT.md             # 开发文档
```

## 核心技术实现

### QuickJS 集成

QuickJS 是一个轻量级的 JavaScript 引擎，我们使用它来执行 Mozilla 的 readability.js：

```python
# 创建 JavaScript 上下文
self._context = Context()
self._context.set_memory_limit(self.memory_limit)
self._context.set_time_limit(self.time_limit)

# 加载 JavaScript 文件
for js_file in js_files:
    js_content = self._load_js_file(js_file)
    self._context.eval(js_content)
```

### JavaScript-Python 数据转换

关键挑战是将 JavaScript 对象转换为 Python 字典：

```python
def _convert_js_result(self, js_result) -> Dict[str, Any]:
    try:
        # 使用 JSON.stringify 转换
        json_fn = self._context.eval("(function(obj) { return JSON.stringify(obj); })")
        json_str = json_fn(js_result)
        return json.loads(json_str)
    except Exception:
        # 回退到直接属性访问
        # ...
```

### DOM 兼容性

由于 JSDOMParser 不支持所有现代 DOM API（如 `querySelectorAll`），我们在包装器中使用了更基本的方法：

```javascript
// 使用 getElementsByTagName 而不是 querySelectorAll
var pElements = document.getElementsByTagName("p");
var preElements = document.getElementsByTagName("pre");
```

## 测试和质量保证

### 运行测试

```bash
# 基本测试
python test_basic.py

# 完整测试套件
pytest tests/

# 测试覆盖率
pytest --cov=fast_readability tests/
```

### 代码格式化

```bash
# 格式化代码
black .
isort .

# 检查代码质量
flake8
mypy fast_readability/
```

## 构建和发布

### 构建包

```bash
python -m build
```

这将在 `dist/` 目录中生成：
- `fast_readability-0.1.0.tar.gz` (源码包)
- `fast_readability-0.1.0-py3-none-any.whl` (wheel包)

### 本地安装

```bash
pip install -e .
```

### 发布到 PyPI

```bash
pip install twine
twine upload dist/*
```

## API 设计原则

### 1. 简单易用
```python
# 最简单的用法
from fast_readability import parse_html
result = parse_html(html_content)
```

### 2. 灵活配置
```python
# 高级配置
with Readability(memory_limit=100*1024*1024, time_limit=30) as reader:
    options = create_custom_options(char_threshold=200, keep_classes=True)
    result = reader.parse(html, url, options)
```

### 3. 错误处理
```python
# 清晰的错误处理
try:
    result = parse_html(html)
except ReadabilityError as e:
    print(f"解析失败: {e}")
```

## 贡献指南

### 添加新功能

1. 在 `fast_readability/` 中添加功能
2. 在 `tests/` 中添加测试
3. 更新文档
4. 确保所有测试通过

### 修复问题

1. 创建复现问题的测试
2. 实现修复
3. 确保测试通过
4. 更新相关文档

### JavaScript 集成

如果需要修改 JavaScript 部分：

1. 修改 `fast_readability/js/readability_wrapper.js`
2. 确保兼容 JSDOMParser 的限制
3. 测试所有功能仍然正常工作

## 性能考虑

### 内存使用
- 默认内存限制：50MB
- 可通过 `memory_limit` 参数调整
- 大文档可能需要增加限制

### 执行时间
- 默认时间限制：10秒
- 可通过 `time_limit` 参数调整
- 复杂文档可能需要更多时间

### 批处理优化
```python
# 重用实例以提高性能
with Readability() as reader:
    for url in urls:
        result = reader.parse_from_url(url)
        # 处理结果
```

## 已知限制

1. **JSDOMParser 限制**: 不支持完整的 DOM API
2. **CSS 选择器**: 不支持复杂的 CSS 选择器
3. **JavaScript 版本**: 使用特定版本的 readability.js
4. **平台兼容性**: 依赖 QuickJS Python 绑定的可用性

## 未来改进

1. **更好的 DOM 支持**: 可能切换到更完整的 JavaScript DOM 实现
2. **性能优化**: 缓存机制、并行处理
3. **更多配置选项**: 暴露更多 readability.js 的配置
4. **插件系统**: 允许自定义内容处理器 