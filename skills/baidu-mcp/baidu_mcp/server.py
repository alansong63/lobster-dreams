"""
百度搜索 MCP 服务器
提供百度网页搜索、百度百科、百度学术、百度新闻四个搜索工具
"""

import asyncio
import json
import re
from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent
import requests
from urllib.parse import quote


class BaiduSearchMCP:
    """百度搜索 MCP 服务器"""
    
    def __init__(self):
        self.app = Server("baidu-mcp")
        self._setup_tools()
    
    def _setup_tools(self):
        """注册所有工具"""
        
        @self.app.call_tool()
        async def baidu_web_search(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """百度网页搜索"""
            query = arguments.get("query", "")
            top_k = arguments.get("top_k", 10)
            
            if not query:
                return [TextContent(type="text", text="错误：缺少必需参数 'query'")]
            
            try:
                results = self._web_search(query, top_k)
                return [TextContent(type="text", text=json.dumps(results, ensure_ascii=False, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=f"搜索失败：{str(e)}")]
        
        @self.app.call_tool()
        async def baidu_baike_search(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """百度百科搜索"""
            keyword = arguments.get("keyword", "")
            
            if not keyword:
                return [TextContent(type="text", text="错误：缺少必需参数 'keyword'")]
            
            try:
                result = self._baike_search(keyword)
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=f"百科搜索失败：{str(e)}")]
        
        @self.app.call_tool()
        async def baidu_scholar_search(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """百度学术搜索"""
            keyword = arguments.get("keyword", "")
            page = arguments.get("page", 0)
            
            if not keyword:
                return [TextContent(type="text", text="错误：缺少必需参数 'keyword'")]
            
            try:
                results = self._scholar_search(keyword, page)
                return [TextContent(type="text", text=json.dumps(results, ensure_ascii=False, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=f"学术搜索失败：{str(e)}")]
        
        @self.app.call_tool()
        async def baidu_news_search(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            """百度新闻搜索"""
            query = arguments.get("query", "")
            top_k = arguments.get("top_k", 10)
            
            if not query:
                return [TextContent(type="text", text="错误：缺少必需参数 'query'")]
            
            try:
                results = self._news_search(query, top_k)
                return [TextContent(type="text", text=json.dumps(results, ensure_ascii=False, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=f"新闻搜索失败：{str(e)}")]
    
    def _web_search(self, query: str, top_k: int = 10) -> dict:
        """百度网页搜索"""
        url = "https://www.baidu.com/s"
        params = {"wd": query, "rn": top_k}
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        
        results = []
        
        # 方法1: 查找 result c-container
        result_pattern = re.compile(r'<div class="result c-container[^>]*>.*?<a[^>]*href="(http[^"]+)"[^>]*>([^<]+)</a>', re.DOTALL)
        for match in result_pattern.findall(response.text)[:top_k]:
            url, title = match
            title = re.sub(r'<.*?>', '', title).strip()
            if title and url:
                results.append({"title": title, "url": url})
        
        # 方法2: 如果方法1没结果，尝试另一种模式
        if not results:
            link_pattern = re.compile(r'<h3[^>]*>.*?<a[^>]*href=["\']([^"\']+(?:baidu\.com/link\?url=[^"\']+)?)["\'][^>]*>([^<]+)</h3>', re.DOTALL)
            for match in link_pattern.findall(response.text)[:top_k]:
                url, title = match
                title = re.sub(r'<.*?>', '', title).strip()
                if title and 'baidu.com/link' in url:
                    results.append({"title": title, "url": url})
        
        return {"query": query, "count": len(results), "results": results}
    
    def _baike_search(self, keyword: str) -> dict:
        """百度百科搜索"""
        url = f"https://baike.baidu.com/item/{quote(keyword)}"
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code != 200 or "baike.baidu.com/error.html" in response.url:
            return {"keyword": keyword, "found": False, "message": "未找到相关百科词条"}
        
        title_pattern = re.compile(r'<h1[^>]*>(.*?)</h1>')
        title_match = title_pattern.search(response.text)
        title = title_match.group(1) if title_match else keyword
        
        summary_pattern = re.compile(r'<div class="lemma-summary">.*?<div class="para">(.*?)</div>', re.DOTALL)
        summary_match = summary_pattern.search(response.text)
        summary = re.sub(r'<.*?>', '', summary_match.group(1)).strip() if summary_match else ""
        
        return {"keyword": keyword, "found": True, "title": title, "summary": summary[:500], "url": response.url}
    
    def _scholar_search(self, keyword: str, page: int = 0) -> dict:
        """百度学术搜索"""
        url = "https://xueshu.baidu.com/s"
        params = {"wd": keyword, "pn": page * 10}
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        results = []
        title_pattern = re.compile(r'<div class="result.*?<a[^>]*href="(.*?)"[^>]*>(.*?)</a>', re.DOTALL)
        for match in title_pattern.findall(response.text)[:10]:
            url, title = match
            title = re.sub(r'<.*?>', '', title).strip()
            if title and url:
                results.append({"title": title, "url": url})
        
        return {"keyword": keyword, "page": page, "count": len(results), "results": results}
    
    def _news_search(self, query: str, top_k: int = 10) -> dict:
        """百度新闻搜索"""
        url = "https://www.baidu.com/s"
        params = {"wd": query, "tn": "news", "rtt": 1, "rn": top_k}
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        results = []
        title_pattern = re.compile(r'<div class="result.*?<a[^>]*href="(.*?)"[^>]*>(.*?)</a>', re.DOTALL)
        for match in title_pattern.findall(response.text)[:top_k]:
            url, title = match
            title = re.sub(r'<.*?>', '', title).strip()
            if title and url:
                results.append({"title": title, "url": url})
        
        return {"query": query, "count": len(results), "results": results}


# 同步入口点 - 供 mcporter 调用
def main():
    """MCP 服务器入口点"""
    import mcp.server.stdio
    
    server_instance = BaiduSearchMCP()
    
    async def run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server_instance.app.run(
                read_stream,
                write_stream,
                server_instance.app.create_initialization_options()
            )
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
