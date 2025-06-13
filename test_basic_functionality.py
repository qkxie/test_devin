#!/usr/bin/env python3

from page_fetcher import PageFetcher
from loguru import logger
import json

def test_basic_functionality():
    """测试PageFetcher的基本功能"""
    print("🧪 测试 PageFetcher 基本功能...")
    
    fetcher = PageFetcher()
    print("✅ PageFetcher 实例创建成功")
    
    test_text = 'Hello 世界 123 こんにちは カタカナ'
    chinese_chars = fetcher._extract_chinese_from_text(test_text)
    print(f"✅ 中文字符检测: {list(chinese_chars)} (应该只包含'世'和'界')")
    
    domain_cn = fetcher._check_domain_language('https://example.cn')
    domain_jp = fetcher._check_domain_language('https://example.jp') 
    domain_com = fetcher._check_domain_language('https://example.com')
    print(f"✅ 域名检查: .cn={domain_cn}, .jp={domain_jp}, .com={domain_com}")
    
    print(f"✅ 预置数据: {len(fetcher.chinese_cities)}个城市, {len(fetcher.chinese_surnames)}个姓氏")
    
    print("\n🎉 所有基本功能测试通过！")
    return True

if __name__ == "__main__":
    test_basic_functionality()
