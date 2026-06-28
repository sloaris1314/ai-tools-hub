#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器自动化演示脚本
展示 Playwright 的自动操作能力
"""

import sys
import time

def demo_browser_automation():
    """演示浏览器自动化功能"""
    print("="*60)
    print("浏览器自动化演示")
    print("="*60)
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("\n[1/5] 启动浏览器...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            print("     浏览器启动成功！")
            
            print("\n[2/5] 创建新页面...")
            page = browser.new_page()
            print("     页面创建成功！")
            
            print("\n[3/5] 访问 ElevenLabs 官网...")
            page.goto("https://elevenlabs.io", timeout=30000)
            time.sleep(2)
            print(f"     页面标题: {page.title()}")
            print(f"     页面 URL: {page.url}")
            
            # 截图
            page.screenshot(path="demo_screenshot1.png")
            print("     截图已保存: demo_screenshot1.png")
            
            print("\n[4/5] 查找页面元素...")
            # 查找所有可能的链接
            links = page.query_selector_all("a")
            print(f"     找到 {len(links)} 个链接")
            
            # 查找包含 "affiliate" 的链接
            affiliate_links = []
            for link in links:
                text = link.inner_text().lower() if link.inner_text() else ""
                if "affiliate" in text or "partner" in text or "refer" in text:
                    affiliate_links.append(link)
            
            if affiliate_links:
                print(f"     找到 {len(affiliate_links)} 个可能的联盟相关链接")
                for i, link in enumerate(affiliate_links[:3]):
                    print(f"     [{i+1}] {link.inner_text()} -> {link.get_attribute('href')}")
            else:
                print("     未找到明显的联盟链接")
                print("     提示: ElevenLabs 联盟可能在页面底部或需要滚动")
            
            print("\n[5/5] 演示自动填表（模拟）...")
            # 打开一个新页面模拟填表
            page.goto("https://elevenlabs.io/affiliates", timeout=15000)
            time.sleep(2)
            print("     已访问联盟页面")
            print("     （实际使用时，这里会自动填写申请表单）")
            
            page.screenshot(path="demo_screenshot2.png")
            print("     截图已保存: demo_screenshot2.png")
            
            print("\n" + "="*60)
            print("演示完成！")
            print("="*60)
            print("\n浏览器将保持打开 10 秒，方便你查看...")
            time.sleep(10)
            
            browser.close()
            print("浏览器已关闭")
            
            return True
            
    except Exception as e:
        print(f"\n[ERROR] 演示失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 设置控制台编码
    sys.stdout.reconfigure(encoding='utf-8')
    
    success = demo_browser_automation()
    
    if success:
        print("\n[SUCCESS] 浏览器自动化演示成功！")
        print("\n接下来可以：")
        print("  1. 手动访问联盟页面，了解申请流程")
        print("  2. 我将根据你的需求定制自动化脚本")
        print("  3. 实现自动填表、自动提交等功能\n")
    else:
        print("\n[ERROR] 请检查 Playwright 安装\n")
    
    sys.exit(0 if success else 1)
