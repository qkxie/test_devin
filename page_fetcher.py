import re
import httpx
from bs4 import BeautifulSoup, Comment
from urllib.parse import urljoin, urlparse
from loguru import logger
from typing import Dict, List, Set, Optional
import asyncio


class PageFetcher:
    def __init__(self):
        self.chinese_cities = {
            '北京', '上海', '广州', '深圳', '杭州', '南京', '苏州', '成都', '武汉', '重庆',
            '天津', '西安', '长沙', '沈阳', '青岛', '郑州', '大连', '东莞', '宁波', '厦门',
            '福州', '无锡', '合肥', '昆明', '哈尔滨', '济南', '佛山', '长春', '温州', '石家庄',
            '南宁', '常州', '泉州', '南昌', '贵阳', '太原', '烟台', '嘉兴', '南通', '金华',
            '珠海', '惠州', '徐州', '海口', '乌鲁木齐', '绍兴', '中山', '台州', '兰州'
        }
        
        self.chinese_surnames = {
            '王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '胡', '朱', '高',
            '林', '何', '郭', '马', '罗', '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
            '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕', '苏', '卢', '蒋', '蔡', '贾',
            '丁', '魏', '薛', '叶', '阎', '余', '潘', '杜', '戴', '夏', '钟', '汪', '田', '任', '姜'
        }
        
        self.common_subpages = ['about', 'privacy', 'contact', 'team', 'company', 'careers']
        
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )

    def __del__(self):
        if hasattr(self, 'client'):
            self.client.close()

    def _is_chinese_char(self, char: str) -> bool:
        """检测是否为中文字符，排除日文假名"""
        code = ord(char)
        if 0x4e00 <= code <= 0x9fff:  # CJK统一汉字
            return True
        if 0x3400 <= code <= 0x4dbf:  # CJK扩展A
            return True
        if 0x20000 <= code <= 0x2a6df:  # CJK扩展B
            return True
        if 0x3040 <= code <= 0x309f:  # 平假名
            return False
        if 0x30a0 <= code <= 0x30ff:  # 片假名
            return False
        return False

    def _extract_chinese_from_text(self, text: str) -> Set[str]:
        """从文本中提取中文字符"""
        chinese_chars = set()
        for char in text:
            if self._is_chinese_char(char):
                chinese_chars.add(char)
        return chinese_chars

    def _check_domain_language(self, url: str) -> Optional[str]:
        """根据域名判断语言"""
        domain = urlparse(url).netloc.lower()
        if '.cn' in domain:
            return 'chinese'
        elif '.jp' in domain:
            return 'non-chinese'
        return None

    def _fetch_page(self, url: str) -> Optional[str]:
        """抓取网页内容"""
        try:
            logger.info(f"正在抓取页面: {url}")
            response = self.client.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"抓取页面失败 {url}: {e}")
            return None

    def _extract_meta_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """提取meta标签信息"""
        meta_info = {}
        
        useful_meta_names = [
            'description', 'keywords', 'author', 'title', 'og:title', 
            'og:description', 'twitter:title', 'twitter:description'
        ]
        
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property')
            content = meta.get('content')
            
            if name and content and name.lower() in useful_meta_names:
                meta_info[name.lower()] = content
                
        return meta_info

    def _extract_external_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, List[str]]:
        """提取外链，特别是LinkedIn、GitHub、X.com"""
        external_links = {
            'linkedin': [],
            'github': [],
            'twitter': [],
            'other': []
        }
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            domain = urlparse(full_url).netloc.lower()
            
            if 'linkedin.com' in domain:
                external_links['linkedin'].append(full_url)
            elif 'github.com' in domain:
                external_links['github'].append(full_url)
            elif 'x.com' in domain or 'twitter.com' in domain:
                external_links['twitter'].append(full_url)
            elif domain and domain != urlparse(base_url).netloc.lower():
                external_links['other'].append(full_url)
                
        return external_links

    def _extract_comments(self, soup: BeautifulSoup) -> Dict[str, Set[str]]:
        """提取HTML、JS、CSS注释中的中文字符"""
        comments_chinese = {
            'html': set(),
            'js': set(),
            'css': set()
        }
        
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            chinese_chars = self._extract_chinese_from_text(comment)
            comments_chinese['html'].update(chinese_chars)
        
        for script in soup.find_all('script'):
            if script.string:
                js_comments = re.findall(r'//.*', script.string)
                js_comments.extend(re.findall(r'/\*.*?\*/', script.string, re.DOTALL))
                
                for comment in js_comments:
                    chinese_chars = self._extract_chinese_from_text(comment)
                    comments_chinese['js'].update(chinese_chars)
        
        for style in soup.find_all('style'):
            if style.string:
                css_comments = re.findall(r'/\*.*?\*/', style.string, re.DOTALL)
                for comment in css_comments:
                    chinese_chars = self._extract_chinese_from_text(comment)
                    comments_chinese['css'].update(chinese_chars)
        
        return comments_chinese

    def _analyze_page_content(self, html: str, url: str) -> Dict:
        """分析页面内容"""
        soup = BeautifulSoup(html, 'html.parser')
        
        page_text = soup.get_text()
        
        chinese_chars = self._extract_chinese_from_text(page_text)
        
        found_cities = set()
        for city in self.chinese_cities:
            if city in page_text:
                found_cities.add(city)
        
        found_surnames = set()
        for surname in self.chinese_surnames:
            if surname in page_text:
                found_surnames.add(surname)
        
        meta_info = self._extract_meta_info(soup)
        
        external_links = self._extract_external_links(soup, url)
        
        comments_chinese = self._extract_comments(soup)
        
        return {
            'chinese_chars': list(chinese_chars),
            'chinese_cities': list(found_cities),
            'chinese_surnames': list(found_surnames),
            'meta_info': meta_info,
            'external_links': external_links,
            'comments_chinese': {k: list(v) for k, v in comments_chinese.items()},
            'has_chinese': len(chinese_chars) > 0 or len(found_cities) > 0 or len(found_surnames) > 0
        }

    def _check_subpages(self, base_url: str) -> Dict:
        """检查子页面"""
        subpage_results = {}
        
        for subpage in self.common_subpages:
            subpage_url = urljoin(base_url, subpage)
            html = self._fetch_page(subpage_url)
            
            if html:
                logger.info(f"分析子页面: {subpage}")
                result = self._analyze_page_content(html, subpage_url)
                if result['has_chinese']:
                    subpage_results[subpage] = result
                    logger.info(f"在子页面 {subpage} 中发现中文内容")
            
        return subpage_results

    def run(self, url: str) -> Dict:
        """主要运行方法"""
        logger.info(f"开始分析网页: {url}")
        
        result = {
            'url': url,
            'is_chinese': False,
            'confidence': 'low',
            'main_page': {},
            'subpages': {},
            'domain_check': None,
            'summary': {}
        }
        
        domain_lang = self._check_domain_language(url)
        result['domain_check'] = domain_lang
        
        if domain_lang == 'chinese':
            logger.info("域名包含.cn，直接判断为中文网站")
            result['is_chinese'] = True
            result['confidence'] = 'high'
            result['summary']['reason'] = '域名包含.cn'
            return result
        elif domain_lang == 'non-chinese':
            logger.info("域名包含.jp，判断为非中文网站")
            result['is_chinese'] = False
            result['confidence'] = 'high'
            result['summary']['reason'] = '域名包含.jp'
            return result
        
        html = self._fetch_page(url)
        if not html:
            logger.error("无法抓取主页面")
            result['summary']['reason'] = '无法抓取页面'
            return result
        
        logger.info("分析主页面内容")
        main_analysis = self._analyze_page_content(html, url)
        result['main_page'] = main_analysis
        
        if main_analysis['has_chinese']:
            logger.info("主页面发现中文内容")
            result['is_chinese'] = True
            result['confidence'] = 'high'
            result['summary']['reason'] = '主页面包含中文内容'
            result['summary']['chinese_indicators'] = {
                'chars_count': len(main_analysis['chinese_chars']),
                'cities_count': len(main_analysis['chinese_cities']),
                'surnames_count': len(main_analysis['chinese_surnames'])
            }
        else:
            logger.info("主页面未发现中文内容，检查子页面")
            subpage_results = self._check_subpages(url)
            result['subpages'] = subpage_results
            
            if subpage_results:
                result['is_chinese'] = True
                result['confidence'] = 'medium'
                result['summary']['reason'] = f'子页面包含中文内容: {list(subpage_results.keys())}'
            else:
                result['is_chinese'] = False
                result['confidence'] = 'medium'
                result['summary']['reason'] = '主页面和子页面均未发现中文内容'
        
        logger.info(f"分析完成，结果: {'中文网站' if result['is_chinese'] else '非中文网站'} (置信度: {result['confidence']})")
        return result
