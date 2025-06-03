import quickjs
import requests
from bs4 import BeautifulSoup
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 读取 JS 脚本
with open("JSDOMParser.js", "r", encoding="utf-8") as f:
    js_dom_parser = f.read()
with open("Readability.js", "r", encoding="utf-8") as f:
    js_readability = f.read()

# 初始化 JS 执行器
ctx = quickjs.Context()
ctx.eval(js_dom_parser)
ctx.eval(js_readability)

# 先用简单HTML测试JSDOMParser
simple_test_js = """
(() => {
    let simple_html = '<html><head><title>Test</title></head><body><p>Hello</p><script>console.log("Hello");</script></body></html>';
    let parser = new JSDOMParser();
    let doc = parser.parse(simple_html);
    
    return JSON.stringify({
        hasDoc: !!doc,
        hasDocumentElement: !!doc.documentElement,
        hasChildNodes: !!doc.childNodes,
        childNodesLength: doc.childNodes ? doc.childNodes.length : 0,
        childNodeNames: doc.childNodes ? doc.childNodes.map(n => n.nodeName) : []
    });
})()
"""

simple_result = ctx.eval(simple_test_js)
print("简单HTML测试:", simple_result)

# 获取网页 HTML
url = "https://1275.ru/ioc/kiberprestupniki-vzlomali-korporativnuyu-set-cherez-uyazvimost-v-confluence-s-posleduyuschim-razvertyvaniem-ransomware_11483"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
html = requests.get(url, headers=headers, verify=False).text
# html = open("test_ru.html", "r", encoding="utf-8").read()

# 用 BeautifulSoup 预处理（可选）
soup = BeautifulSoup(html, "html.parser")

# 使用BeautifulSoup重新格式化HTML，确保结构正确
# 查找所有 script 标签并删除
for script in soup.find_all('script'):
    script.decompose() # decompose() 方法会完全移除标签及其内容

# 查找所有带有style属性的标签
for tag in soup.find_all(style=True):
    # 删除style属性
    del tag['style']

clean_html = str(soup.html)

# 检查HTML内容
print("HTML开头:", repr(html[:200]))
print("HTML是否包含<html>:", "<html" in html.lower())
print("HTML长度:", len(html))
print("清理后HTML开头:", repr(clean_html[:200]))
print("清理后HTML结尾:", repr(clean_html[-200:]))

# 构建 JS 执行代码（确保使用 JS 字符串语法）
escaped_html = json.dumps(clean_html)  # 使用清理后的HTML（移除了script和style）

# 先检查解析是否正常
debug_js = f"""
(() => {{
    let parser = new JSDOMParser();
    let doc = parser.parse({escaped_html});
    
    return JSON.stringify({{
        hasDoc: !!doc,
        hasDocumentElement: !!doc.documentElement,
        hasChildNodes: !!doc.childNodes,
        childNodesLength: doc.childNodes ? doc.childNodes.length : 0,
        childNodeNames: doc.childNodes ? doc.childNodes.map(n => n.nodeName) : []
    }});
}})()
"""

debug_result = ctx.eval(debug_js)
print("Debug info:", debug_result)


js_code = f"""
(() => {{
    let parser = new JSDOMParser();
    let doc = parser.parse({escaped_html});
    
    // 如果没有documentElement，但有childNodes，手动设置documentElement
    if (!doc.documentElement && doc.childNodes && doc.childNodes.length > 0) {{
        for (let i = 0; i < doc.childNodes.length; i++) {{
            if (doc.childNodes[i].nodeName === 'HTML') {{
                doc.documentElement = doc.childNodes[i];
                break;
            }}
        }}
    }}
    
    let reader = new Readability(doc);
    let article = reader.parse();
    return JSON.stringify(article);
}})()
"""

# 执行并返回结果
result_json = ctx.eval(js_code)
result = json.loads(result_json)

# 输出标题与正文
print("标题:", result["title"])
print("正文片段:", result["content"])  # HTML 格式内容
