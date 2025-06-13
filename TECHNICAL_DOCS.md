# PageFetcher 技术文档

## 架构设计

### 类结构

```
PageFetcher
├── __init__()              # 初始化配置和数据
├── run(url)               # 主入口方法
├── _fetch_page(url)       # 网页抓取
├── _analyze_page_content() # 页面内容分析
├── _extract_meta_info()   # Meta信息提取
├── _extract_external_links() # 外链提取
├── _extract_comments()    # 注释分析
├── _check_subpages()      # 子页面检查
├── _is_chinese_char()     # 中文字符判断
├── _extract_chinese_from_text() # 文本中文提取
└── _check_domain_language() # 域名语言判断
```

## 核心算法

### 1. 中文字符检测

```python
def _is_chinese_char(self, char: str) -> bool:
    code = ord(char)
    # CJK统一汉字: 0x4e00-0x9fff
    # CJK扩展A: 0x3400-0x4dbf  
    # CJK扩展B: 0x20000-0x2a6df
    # 排除日文假名: 0x3040-0x309f (平假名), 0x30a0-0x30ff (片假名)
```

### 2. 置信度计算逻辑

- **High**: 域名明确指示(.cn/.jp) 或 主页面有明显中文内容
- **Medium**: 子页面发现中文内容 或 主页面无中文但有其他指标
- **Low**: 无法确定或网络错误

### 3. 子页面检测策略

检测常见子页面: `['about', 'privacy', 'contact', 'team', 'company', 'careers']`

## 数据结构

### 中国城市列表 (部分)
```python
chinese_cities = {
    '北京', '上海', '广州', '深圳', '杭州', '南京', '苏州', 
    '成都', '武汉', '重庆', '天津', '西安', '长沙', ...
}
```

### 中文姓氏列表 (部分)  
```python
chinese_surnames = {
    '王', '李', '张', '刘', '陈', '杨', '赵', '黄', 
    '周', '吴', '徐', '孙', '胡', '朱', '高', ...
}
```

## 网络请求配置

```python
client = httpx.Client(
    timeout=30.0,           # 30秒超时
    follow_redirects=True,  # 自动跟随重定向
    headers={
        'User-Agent': 'Mozilla/5.0 ...'  # 模拟浏览器
    }
)
```

## 错误处理

1. **网络错误**: 连接超时、DNS解析失败等
2. **解析错误**: HTML格式错误、编码问题等  
3. **内容错误**: 空页面、无效内容等

每种错误都会记录详细日志并返回相应的错误状态。

## 性能优化

1. **并发控制**: 使用单个 httpx.Client 实例复用连接
2. **内存管理**: 及时清理大型HTML文档
3. **请求优化**: 合理的超时设置和重试机制
4. **缓存策略**: 可扩展添加结果缓存

## 扩展性设计

### 添加新的检测规则

```python
def _check_custom_indicator(self, text: str) -> bool:
    # 添加自定义检测逻辑
    pass
```

### 添加新的子页面

```python
self.common_subpages.extend(['新页面1', '新页面2'])
```

### 自定义外链平台

```python
# 在 _extract_external_links 方法中添加新平台检测
if 'newplatform.com' in domain:
    external_links['newplatform'].append(full_url)
```

## 日志系统

使用 loguru 提供结构化日志:

- **INFO**: 正常流程信息
- **ERROR**: 错误和异常
- **DEBUG**: 详细调试信息

日志格式包含时间戳、级别、文件位置和消息内容。

## 测试策略

1. **单元测试**: 测试各个独立方法
2. **集成测试**: 测试完整流程
3. **边界测试**: 测试异常情况和边界条件
4. **性能测试**: 测试大量网站的处理能力

## 安全考虑

1. **请求限制**: 避免过于频繁的请求
2. **内容过滤**: 防止恶意内容注入
3. **资源限制**: 限制下载文件大小
4. **隐私保护**: 不记录敏感信息

## 依赖管理

- **httpx**: 现代异步HTTP客户端
- **beautifulsoup4**: HTML解析库
- **loguru**: 现代日志库
- **lxml**: 高性能XML/HTML解析器

所有依赖都是稳定的、维护良好的开源项目。
