---
name: zh-search
description: Default Chinese web search using Baidu AI Search API. Activate when user needs to search the web in Chinese or for Chinese content.
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["python3"], "env": ["BAIDU_API_KEY"] }, "primaryEnv": "BAIDU_API_KEY" } }
---

# 中文搜索

默认中文网络搜索，使用百度千帆 AI Search API。

## 使用场景

当用户需要：
- 搜索中文内容
- 查询中文资讯、新闻
- 搜索中国本地化信息
- 任何需要中文搜索结果的情况

## 使用方式

```bash
python3 skills/zh-search/scripts/search.py '<JSON>'
```

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | 是 | - | 搜索关键词 |
| edition | string | 否 | standard | standard（完整）或 lite（轻量） |
| search_recency_filter | string | 否 | year | 时间过滤：week, month, semiyear, year |
| resource_type_filter | list | 否 | web:20 | 资源类型：web(50), video(10), image(30), aladdin(5) |
| search_filter | object | 否 | - | 高级过滤（见下方） |
| block_websites | list | 否 | - | 屏蔽网站，如 ["tieba.baidu.com"] |
| safe_search | boolean | 否 | false | 开启严格内容过滤 |

## search_filter 高级用法

```json
{
  "search_filter": {
    "match": {
      "site": ["zhihu.com", "baike.baidu.com"]
    }
  }
}
```

## 示例

```bash
# 基础搜索
python3 skills/zh-search/scripts/search.py '{"query":"人工智能最新进展"}'

# 最近一周的新闻
python3 skills/zh-search/scripts/search.py '{"query":"科技新闻","search_recency_filter":"week"}'

# 限定网站
python3 skills/zh-search/scripts/search.py '{"query":"Python教程","search_filter":{"match":{"site":["www.zhihu.com"]}}}'
```

## 当前状态

完全可用，作为默认中文搜索工具。
