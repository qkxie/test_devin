# PageFetcher - 网页中文属性分析工具

## 功能特性

PageFetcher 是一个用于分析网页是否具有明显中文属性的 Python 类，具备以下功能：

1. **网页抓取**: 使用 httpx 抓取网页内容，支持重定向
2. **HTML解析**: 使用 Beautiful Soup 解析 HTML 内容
3. **Meta信息提取**: 提取网页中的 meta 标签内容（排除无关信息）
4. **外链提取**: 提取页面中的外链，特别关注 LinkedIn、GitHub、X.com (Twitter)
5. **注释分析**: 提取 HTML、JS、CSS 注释中的中文字符
6. **中文检测**: 检测页面中的中文字符（排除日文假名）、中国城市名、常见中文姓氏
7. **子页面分析**: 如果主页面没有中文，会抓取 about、privacy 等常见子页面继续判断
8. **域名判断**: 域名含 .cn 直接判断为中文；含 .jp 判断为非中文
9. **结构化输出**: 返回详细的结构化字典结果
10. **日志记录**: 使用 loguru 打印详细日志

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```python
from page_fetcher import PageFetcher

# 创建实例
fetcher = PageFetcher()

# 分析网页
result = fetcher.run("https://www.example.com")

# 查看结果
print(f"是否为中文网站: {result['is_chinese']}")
print(f"置信度: {result['confidence']}")
print(f"判断依据: {result['summary']['reason']}")
```

### 返回结果结构

```python
{
    'url': '分析的网址',
    'is_chinese': True/False,  # 是否为中文网站
    'confidence': 'high/medium/low',  # 置信度
    'main_page': {
        'chinese_chars': ['中', '文', '字', '符'],
        'chinese_cities': ['北京', '上海'],
        'chinese_surnames': ['王', '李'],
        'meta_info': {'description': '...', 'keywords': '...'},
        'external_links': {
            'linkedin': ['...'],
            'github': ['...'],
            'twitter': ['...'],
            'other': ['...']
        },
        'comments_chinese': {
            'html': ['中', '文'],
            'js': ['注', '释'],
            'css': ['样', '式']
        },
        'has_chinese': True/False
    },
    'subpages': {
        'about': {...},  # 子页面分析结果
        'privacy': {...}
    },
    'domain_check': 'chinese/non-chinese/null',
    'summary': {
        'reason': '判断依据',
        'chinese_indicators': {
            'chars_count': 100,
            'cities_count': 5,
            'surnames_count': 10
        }
    }
}
```

## 测试示例

运行测试脚本：

```bash
python test_page_fetcher.py
```

## 类设计特点

- **职责单一**: 每个方法都有明确的单一职责
- **结构清晰**: 代码组织良好，易于理解和维护
- **错误处理**: 完善的异常处理机制
- **日志记录**: 详细的日志记录，便于调试
- **可扩展性**: 易于添加新的检测规则和功能

## 主要方法说明

- `run(url)`: 主要入口方法，返回完整分析结果
- `_fetch_page(url)`: 抓取网页内容
- `_analyze_page_content(html, url)`: 分析页面内容
- `_extract_meta_info(soup)`: 提取 meta 信息
- `_extract_external_links(soup, base_url)`: 提取外链
- `_extract_comments(soup)`: 提取注释中的中文
- `_check_subpages(base_url)`: 检查子页面
- `_is_chinese_char(char)`: 判断是否为中文字符
- `_check_domain_language(url)`: 根据域名判断语言

## 注意事项

1. 网络请求可能会超时，建议在网络环境良好的情况下使用
2. 某些网站可能有反爬虫机制，可能需要调整请求头或添加延时
3. 日文假名已被排除在中文字符检测之外
4. 子页面检测会增加请求次数，请合理使用
