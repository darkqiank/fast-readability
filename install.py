#!/usr/bin/env python3
"""
Fast Readability 安装辅助脚本
"""

import subprocess
import sys
import os

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要 Python 3.7 或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    else:
        print(f"✓ Python 版本检查通过: {sys.version}")
        return True

def install_dependencies():
    """安装依赖包"""
    try:
        print("正在安装依赖包...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 依赖包安装失败: {e}")
        return False

def install_package():
    """安装包"""
    try:
        print("正在安装 fast-readability 包...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
        print("✓ 包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 包安装失败: {e}")
        return False

def run_tests():
    """运行测试"""
    try:
        print("正在运行测试...")
        subprocess.check_call([sys.executable, "test_package.py"])
        print("✓ 测试通过")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """主安装流程"""
    print("Fast Readability 安装程序")
    print("=" * 40)
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not install_package():
        sys.exit(1)
    
    if not run_tests():
        print("警告: 测试失败，但安装可能已完成")
    
    print("\n" + "=" * 40)
    print("安装完成！")
    print("\n使用示例:")
    print("  python examples/basic_usage.py")
    print("\nPython 代码示例:")
    print("  from fast_readability import Readability")
    print("  reader = Readability()")
    print("  result = reader.extract_from_url('https://example.com')")
    print("  print(result['title'])")

if __name__ == "__main__":
    main() 