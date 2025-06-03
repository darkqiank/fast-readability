#!/usr/bin/env python3
"""
测试 fast_readability 包的基本功能
"""

import sys
import os

# 添加当前目录到路径，以便导入本地包
sys.path.insert(0, os.path.dirname(__file__))

def test_import():
    """测试包导入"""
    try:
        from fast_readability import Readability, extract_content
        print("✓ 包导入成功")
        return True
    except ImportError as e:
        print(f"✗ 包导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    try:
        from fast_readability import Readability
        
        # 简单的HTML测试
        html = """
        <html>
        <head><title>测试标题</title></head>
        <body>
            <article>
                <h1>测试文章</h1>
                <p>这是一段测试内容，用于验证HTML内容提取功能是否正常工作。</p>
                <p>这里是第二段内容，增加一些文字以确保内容长度足够。</p>
            </article>
        </body>
        </html>
        """
        
        reader = Readability(debug=True)
        result = reader.extract_from_html(html)
        
        if result['title']:
            print(f"✓ 标题提取成功: {result['title']}")
        else:
            print("✗ 标题提取失败")
            return False
            
        if result['textContent']:
            print(f"✓ 内容提取成功: {len(result['textContent'])} 字符")
        else:
            print("✗ 内容提取失败")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def test_utility_functions():
    """测试实用函数"""
    try:
        from fast_readability import extract_content
        
        html = "<html><head><title>实用函数测试</title></head><body><p>测试内容</p></body></html>"
        result = extract_content(html)
        
        if result and result.get('title'):
            print("✓ 便捷函数测试成功")
            return True
        else:
            print("✗ 便捷函数测试失败")
            return False
            
    except Exception as e:
        print(f"✗ 便捷函数测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Fast Readability 包测试")
    print("=" * 40)
    
    all_passed = True
    
    # 测试导入
    if not test_import():
        all_passed = False
        return
    
    # 测试基本功能
    if not test_basic_functionality():
        all_passed = False
    
    # 测试实用函数
    if not test_utility_functions():
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ 所有测试通过！")
    else:
        print("✗ 部分测试失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 