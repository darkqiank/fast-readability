#!/usr/bin/env python3
"""
Fast Readability 基本使用示例
"""

import sys
import os

# 添加父目录到路径，以便导入包
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fast_readability import Readability, extract_content


def demo_html_extraction():
    """演示从HTML字符串提取内容"""
    print("=== HTML字符串提取示例 ===")
    
    html = """
    <html>
    <head>
        <title>示例文章</title>
        <meta charset="utf-8">
    </head>
    <body>
        <header>
            <nav>导航栏 - 这部分会被过滤</nav>
        </header>
        
        <article>
            <h1>Python Web爬虫入门指南</h1>
            <p class="byline">作者：张三 | 发布时间：2024-01-01</p>
            
            <p>Web爬虫是一种自动获取网页数据的程序。Python因其简洁的语法和丰富的库支持，成为了爬虫开发的首选语言。</p>
            
            <h2>什么是Web爬虫？</h2>
            <p>Web爬虫（Web Crawler）是一种按照一定的规则，自动地抓取网络信息的程序或者脚本。它们被广泛用于搜索引擎索引、数据挖掘、监测网站变化等领域。</p>
            
            <h2>Python爬虫的优势</h2>
            <ul>
                <li>语法简洁，易于学习</li>
                <li>有强大的第三方库支持</li>
                <li>社区活跃，文档丰富</li>
            </ul>
            
            <p>总之，Python是进行Web爬虫开发的理想选择。无论是初学者还是专业开发者，都能够快速上手并构建高效的爬虫应用。</p>
        </article>
        
        <aside>
            <h3>相关文章</h3>
            <ul>
                <li><a href="#">数据分析入门</a></li>
                <li><a href="#">机器学习基础</a></li>
            </ul>
        </aside>
        
        <footer>
            <p>版权所有 © 2024 示例网站</p>
        </footer>
    </body>
    </html>
    """
    
    # 使用类方法
    reader = Readability(debug=True)
    result = reader.extract_from_html(html)
    
    print(f"标题: {result['title']}")
    print(f"作者信息: {result['byline']}")
    print(f"内容长度: {result['length']} 字符")
    print(f"摘要: {result['excerpt']}")
    print("\n--- 正文内容 ---")
    print(result['textContent'][:300] + "..." if len(result['textContent']) > 300 else result['textContent'])
    
    # 使用便捷函数
    print("\n=== 使用便捷函数 ===")
    result2 = extract_content(html)
    print(f"便捷函数提取的标题: {result2['title']}")


def demo_utility_methods():
    """演示实用方法"""
    print("\n=== 实用方法示例 ===")
    
    html = """
    <html>
    <head><title>测试页面</title></head>
    <body>
        <h1>这是一个测试页面</h1>
        <p>这里有一些内容用于测试各种实用方法。</p>
        <p>内容应该足够长以通过可读性检查。</p>
    </body>
    </html>
    """
    
    reader = Readability()
    
    # 获取标题
    title = reader.get_title(html)
    print(f"标题: {title}")
    
    # 获取纯文本内容
    text_content = reader.get_text_content(html)
    print(f"纯文本: {text_content}")
    
    # 检查是否可读
    is_readable = reader.is_probably_readable(html)
    print(f"是否可读: {is_readable}")
    
    # 检查短内容
    short_html = "<html><body><p>太短了</p></body></html>"
    is_short_readable = reader.is_probably_readable(short_html)
    print(f"短内容是否可读: {is_short_readable}")


def main():
    """主函数"""
    print("Fast Readability 使用示例")
    print("=" * 50)
    
    demo_html_extraction()
    demo_utility_methods()
    
    print("\n示例演示完成！")


if __name__ == "__main__":
    main() 