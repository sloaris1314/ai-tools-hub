#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动测试自动发布流程：生成一篇新文章 + 推送到 GitHub
"""
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

CWD = "H:/AI工作文件夹/赚钱/ai-affiliate-site"

def run(cmd, cwd=CWD):
    """运行命令并返回输出"""
    result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, encoding='utf-8')
    print(f"$ {cmd}")
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"[stderr] {result.stderr}")
    return result.returncode == 0

def main():
    print("=" * 60)
    print("手动测试自动发布流程")
    print("=" * 60)
    
    # 生成一篇测试文章（Perplexity AI 评测）
    article_slug = "perplexity-ai-guide"
    article_title = "Perplexity AI 完全指南：会思考的搜索引擎，替代Google？"
    article_date = datetime.now().strftime("%Y-%m-%d")
    article_file = f"articles/{article_slug}.html"
    
    print(f"\n[1/4] 生成测试文章: {article_title}")
    
    # 读取模板
    template_path = Path(CWD) / "article-template.html"
    template = template_path.read_text(encoding='utf-8')
    
    # 文章内容
    content = """
<p>如果你已经厌倦了在Google搜索结果里翻页、筛选广告和低质量内容，Perplexity AI 可能是2026年最值得尝试的搜索工具。它不是传统的搜索引擎，而是一个"会回答问题的 AI"——直接给你带引用来源的答案。</p>

<h2>Perplexity AI 是什么？</h2>
<p>Perplexity AI 是一个基于大语言模型的对话式搜索引擎。与 Google 不同，它不会返回一堆链接让你自己找答案，而是直接生成一段总结性回答，并在每个关键信息后面标注来源链接。</p>

<h2>核心功能</h2>
<ul>
<li><strong>实时联网搜索</strong>：Perplexity 会实时检索互联网，不是只依赖训练数据</li>
<li><strong>答案带引用</strong>：每个关键信息都有可点击的引用来源，方便验证</li>
<li><strong>多轮对话</strong>：可以基于之前的回答继续追问，像和研究员对话一样</li>
<li><strong>专注模式</strong>：可以限定搜索范围（学术、Reddit、YouTube、新闻等）</li>
<li><strong>Pro 搜索</strong>：付费版支持更复杂的查询和更多模型选择</li>
</ul>

<h2>使用场景</h2>
<ul>
<li>快速了解一个新话题</li>
<li>写报告时收集资料和引用</li>
<li>需要最新信息（股票、新闻、产品发布）</li>
<li>替代传统搜索引擎进行深度研究</li>
</ul>

<h2>优缺点</h2>
<table class="rating-table">
<tr><th>优点</th><th>缺点</th></tr>
<tr><td>答案直接，节省时间</td><td>复杂问题可能过度简化</td></tr>
<tr><td>引用来源可验证</td><td>免费版有查询次数限制</td></tr>
<tr><td>界面简洁，无广告</td><td>某些小众主题信息覆盖不足</td></tr>
</table>

<h2>与 Google 的区别</h2>
<p>Google 给你 10 个蓝色链接，Perplexity 给你一个带引用的答案。前者适合浏览和探索，后者适合快速获取准确信息。两者不是完全替代关系，但 Perplexity 在研究型查询上明显更高效。</p>

<h2>总结评分</h2>
<ul>
<li><strong>搜索体验</strong>：★★★★★</li>
<li><strong>答案质量</strong>：★★★★☆</li>
<li><strong>信息新鲜度</strong>：★★★★★</li>
<li><strong>性价比</strong>：★★★★☆</li>
</ul>
<p>Perplexity 是2026年每个知识工作者都值得尝试的工具。它可能不会完全替代 Google，但绝对是研究、学习和工作查资料时的首选工具之一。</p>
"""
    
    # 替换模板变量
    html = template.replace("ARTICLE_TITLE", article_title)
    html = html.replace("ARTICLE_EXCERPT", "Perplexity AI 使用指南：会实时联网、带引用来源的AI搜索引擎，帮你快速找到准确答案。")
    html = html.replace("ARTICLE_CATEGORY", "AI写作")
    html = html.replace("ARTICLE_DATE", article_date)
    html = html.replace("ARTICLE_READTIME", "6")
    html = html.replace("ARTICLE_CONTENT", content)
    html = html.replace("ARTICLE_TOOL_NAME", "Perplexity")
    html = html.replace("ARTICLE_BONUS", "更智能的搜索体验")
    html = html.replace("ARTICLE_AFFILIATE_LINK", "https://perplexity.ai?ref=AFF_PLACEHOLDER")
    
    # 保存文章
    article_path = Path(CWD) / article_file
    article_path.write_text(html, encoding='utf-8')
    print(f"[OK] 文章已保存: {article_path}")
    
    # 更新首页 index.html
    print("\n[2/4] 更新首页文章列表...")
    index_path = Path(CWD) / "index.html"
    index_html = index_path.read_text(encoding='utf-8')
    
    new_card = f'''
      <div class="article-card" onclick="location.href='articles/{article_slug}.html'">
        <div class="article-thumb">🔍</div>
        <div class="article-body">
          <div class="article-meta"><span>AI写作</span></div>
          <div class="article-title">{article_title}</div>
          <div class="article-excerpt">Perplexity AI 使用指南：会实时联网、带引用来源的AI搜索引擎，帮你快速找到准确答案。</div>
          <div class="article-footer">
            <span class="article-date">{article_date}</span>
            <span class="article-read">阅读全文 →</span>
          </div>
        </div>
      </div>
'''
    
    # 在 articles-grid 开头插入新卡片
    marker = '<div class="articles-grid">\n'
    index_html = index_html.replace(marker, marker + '\n' + new_card)
    index_path.write_text(index_html, encoding='utf-8')
    print("[OK] 首页已更新")
    
    # 更新 sitemap.xml
    print("\n[3/4] 更新 sitemap.xml...")
    sitemap_path = Path(CWD) / "sitemap.xml"
    sitemap = sitemap_path.read_text(encoding='utf-8')
    
    new_url = f"""    <url>
        <loc>https://sloaris1314.github.io/ai-tools-hub/articles/{article_slug}.html</loc>
        <lastmod>{article_date}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
"""
    sitemap = sitemap.replace("</urlset>", new_url + "</urlset>")
    sitemap_path.write_text(sitemap, encoding='utf-8')
    print("[OK] sitemap 已更新")
    
    # Git 提交并推送
    print("\n[4/4] 推送到 GitHub...")
    run("git add .")
    run(f"git commit -m \"Auto publish: {article_title}\"")
    success = run("git push origin main")
    
    if success:
        print("\n" + "=" * 60)
        print("[SUCCESS] 发布流程测试通过！")
        print(f"文章地址: https://sloaris1314.github.io/ai-tools-hub/articles/{article_slug}.html")
        print("=" * 60)
    else:
        print("\n[ERROR] Git push 失败")
    
    return success

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    success = main()
    sys.exit(0 if success else 1)
