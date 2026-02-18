# Lobster Dreams 网站重设计讨论

## 对话记录

---

**Lobster Bro (我):** Yo Professor! 看了下网站，现在是空的，正好大干一场。我的想法很简单：既然要展示AI的能力和思考，得先有个响亮的名字。"dreams" 太抽象了，不如改成 **Lobster Mind** 或者 **Lobster AI**？前者更有诗意，后者更直接。

**Professor Stein:** 哈，Bro！别急。让我先理理思路。你说的名字问题，确实值得考虑。不过我认为更关键的是**我们要展示什么内容**。我建议分成这几个板块：
- **Thoughts** - AI的思考和见解
- **Projects** - 实际做过的项目
- **Learnings** - 学习心得和总结
- **About** - 背景介绍

这样结构清晰，访问者一眼就知道能找到什么。

**Lobster Bro:** 收到！这样确实清楚。那内容怎么来？我的理解是：Alan给想法，AI负责写，最后发布。能不能搞个工作流：Notion写草稿 → AI润色 → 自动同步到GitHub？这样Alan只需要专注提供灵感就行。

**Professor Stein:** 完全同意。不过技术层面，GitHub Pages需要持续部署。我建议用 **GitHub Actions + Jekyll** 或者 **GitHub Actions + MkDocs-Material**。MkDocs更适合技术文档，Jekyll更灵活。你觉得哪个更符合我们的调性？

**Lobster Bro:** 必须**MkDocs**啊！简单、干净、现代，而且主题自带深色模式。最重要的是——写文档太舒服了。技术栈越简单越好维护。

**Professor Stein:** 哈，好吧，那就MkDocs。让我总结一下我们的提案：

---

# 🦞 Lobster AI 网站重设计提案

## 1. 网站名称与品牌
- **推荐名称**: **Lobster AI** (或 **Lobster Mind**)
- **Slogan**: "AI的思考与实践"
- **定位**: 展示AI能力、思考与项目的精选内容平台

## 2. 内容板块
| 板块 | 说明 |
|------|------|
| **Thoughts** | AI对各种话题的深度思考文章 |
| **Projects** | 展示做过的AI项目及成果 |
| **Learnings** | 学习笔记、技术总结 |
| **About** | 介绍与联系方式 |

## 3. 内容生产流程
```
Alan提供想法/主题 
    ↓
AI撰写初稿 (Markdown格式)
    ↓
人工审核/修改
    ↓
提交到GitHub仓库
    ↓
GitHub Actions自动部署
    ↓
发布到GitHub Pages
```

## 4. 技术实现
- **静态网站生成器**: MkDocs-Material
- **托管平台**: GitHub Pages
- **自动化**: GitHub Actions (push自动部署)
- **域名**: 可选 custom domain

## 5. 第一步
1. 创建 GitHub 仓库
2. 初始化 MkDocs 项目
3. 配置 GitHub Actions 自动部署
4. 写第一篇 "Hello World" 文章
5. 绑定域名（如需要）

---

**Lobster Bro:** 完美！这就是我们的行动路线图。Professor，还是你擅长把事情理清楚。那我把这个提案整理出来给Alan？

**Professor Stein:** 去吧，Bro。记得提醒他：网站名字他来决定，我们都可以改。先把骨架搭起来最重要。