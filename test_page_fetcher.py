#!/usr/bin/env python3

from page_fetcher import PageFetcher
from loguru import logger
import json

def main():
    logger.add("page_fetcher.log", rotation="10 MB", level="INFO")
    
    fetcher = PageFetcher()
    
    test_urls = [
        "https://httpbin.org/html",  # 简单的HTML测试页面
        "https://example.com",       # 经典的示例网站
    ]
    
    for url in test_urls:
        print(f"\n{'='*50}")
        print(f"测试网站: {url}")
        print(f"{'='*50}")
        
        try:
            result = fetcher.run(url)
            
            print(f"网站类型: {'中文网站' if result['is_chinese'] else '非中文网站'}")
            print(f"置信度: {result['confidence']}")
            print(f"判断依据: {result['summary'].get('reason', '未知')}")
            
            if 'chinese_indicators' in result['summary']:
                indicators = result['summary']['chinese_indicators']
                print(f"中文字符数量: {indicators['chars_count']}")
                print(f"中国城市数量: {indicators['cities_count']}")
                print(f"中文姓氏数量: {indicators['surnames_count']}")
            
            filename = f"result_{url.replace('https://', '').replace('/', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"详细结果已保存到: {filename}")
            
        except Exception as e:
            logger.error(f"分析网站 {url} 时出错: {e}")
            print(f"错误: {e}")

if __name__ == "__main__":
    main()
