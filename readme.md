# Test Devin Repository

This is a test repository for verifying Devin's capabilities:
- Repository access ✓
- Branch creation ✓
- File modification ✓
- Lint verification (in progress)
- PR creation (pending)

## Projects

### PageFetcher - 网页中文属性分析工具

一个用于分析网页是否具有明显中文属性的 Python 类。

#### 主要功能
- 使用 httpx 抓取网页内容，支持重定向
- 使用 Beautiful Soup 解析 HTML
- 提取 meta 标签和外链信息
- 检测中文字符、中国城市名、中文姓氏
- 分析 HTML/JS/CSS 注释中的中文内容
- 智能子页面检测
- 基于域名的语言判断
- 结构化结果输出和详细日志

#### 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 基本使用
from page_fetcher import PageFetcher
fetcher = PageFetcher()
result = fetcher.run('https://example.com')
print(f'是否为中文网站: {result["is_chinese"]}')

# 运行示例
python example_usage.py
```

#### 文档
- [使用说明](README_PageFetcher.md)
- [技术文档](TECHNICAL_DOCS.md)

## Simple Test Change

This change demonstrates basic Git workflow functionality.
