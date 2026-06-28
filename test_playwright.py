#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 测试脚本 - 验证浏览器自动化环境
"""

import sys
import os

def test_playwright():
    """测试 Playwright 是否能正常启动浏览器"""
    print("[TEST] 开始测试 Playwright...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("[TEST] Playwright 模块加载成功")
        print("[TEST] 启动浏览器...")
        
        with sync_playwright() as p:
            # 启动有界面的浏览器（这样你能看到）
            browser = p.chromium.launch(headless=False)
            print("[TEST] 浏览器启动成功！")
            
            # 打开一个新页面
            page = browser.new_page()
            print("[TEST] 创建新页面成功")
            
            # 访问测试页面
            print("[TEST] 正在访问 https://example.com ...")
            page.goto("https://example.com", timeout=15000)
            print(f"[TEST] 页面标题: {page.title()}")
            print(f"[TEST] 页面 URL: {page.url}")
            
            # 截图保存
            screenshot_path = "H:/AI工作文件夹/赚钱/ai-affiliate-site/test_screenshot.png"
            page.screenshot(path=screenshot_path)
            print(f"[TEST] 截图已保存到: {screenshot_path}")
            
            # 关闭浏览器
            browser.close()
            print("[TEST] 浏览器已关闭")
            print("\n[SUCCESS] Playwright 测试通过！浏览器自动化环境正常")
            return True
            
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # 设置控制台输出编码为 UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("Playwright 环境测试")
    print("=" * 60)
    
    success = test_playwright()
    
    if success:
        print("\n[READY] 可以开始使用浏览器自动化工具了！")
    else:
        print("\n[ERROR] 请检查 Playwright 安装")
        
    sys.exit(0 if success else 1)
