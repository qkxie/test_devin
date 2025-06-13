#!/usr/bin/env python3
"""
PageFetcher 使用示例
演示如何使用 PageFetcher 类分析不同类型的网站
"""

from page_fetcher import PageFetcher
from loguru import logger
import json
import sys

def analyze_website(fetcher, url, description=""):
    """分析单个网站并打印结果"""
    print(f"\n{'='*60}")
    print(f"分析网站: {url}")
    if description:
        print(f"描述: {description}")
    print(f"{'='*60}")
    
    try:
        result = fetcher.run(url)
        
        print(f"✓ 网站类型: {'🇨🇳 中文网站' if result['is_chinese'] else '🌍 非中文网站'}")
        print(f"✓ 置信度: {result['confidence']}")
        print(f"✓ 判断依据: {result['summary'].get('reason', '未知')}")
        
        if result['domain_check']:
            print(f"✓ 域名检查: {result['domain_check']}")
        
        main_page = result['main_page']
        if main_page:
            print(f"\n📄 主页面分析:")
            print(f"  - 中文字符数: {len(main_page.get('chinese_chars', []))}")
            print(f"  - 中国城市数: {len(main_page.get('chinese_cities', []))}")
            print(f"  - 中文姓氏数: {len(main_page.get('chinese_surnames', []))}")
            
            if main_page.get('chinese_cities'):
                print(f"  - 发现的城市: {', '.join(main_page['chinese_cities'][:5])}")
            if main_page.get('chinese_surnames'):
                print(f"  - 发现的姓氏: {', '.join(main_page['chinese_surnames'][:5])}")
            
            external_links = main_page.get('external_links', {})
            if any(external_links.values()):
                print(f"  - 外链统计:")
                for platform, links in external_links.items():
                    if links:
                        print(f"    * {platform}: {len(links)} 个链接")
        
        if result['subpages']:
            print(f"\n📑 子页面分析:")
            for subpage, data in result['subpages'].items():
                print(f"  - {subpage}: 发现中文内容")
        
        return result
        
    except Exception as e:
        logger.error(f"分析网站 {url} 时出错: {e}")
        print(f"❌ 错误: {e}")
        return None

def main():
    """主函数"""
    logger.remove()  # 移除默认处理器
    logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    logger.add("page_fetcher_example.log", rotation="10 MB", level="DEBUG")
    
    print("🚀 PageFetcher 网页中文属性分析工具")
    print("=" * 60)
    
    fetcher = PageFetcher()
    
    test_cases = [
        {
            "url": "https://httpbin.org/html",
            "description": "简单的HTML测试页面"
        },
        {
            "url": "https://example.com",
            "description": "经典的示例网站"
        }
    ]
    
    results = []
    
    for case in test_cases:
        result = analyze_website(fetcher, case["url"], case["description"])
        if result:
            results.append(result)
    
    if results:
        with open("analysis_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 所有分析结果已保存到: analysis_results.json")
    
    print(f"\n✅ 分析完成！共分析了 {len(results)} 个网站")

if __name__ == "__main__":
    main()
