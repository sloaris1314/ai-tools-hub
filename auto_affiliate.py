#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 联盟申请自动化工具 v1.0
功能：自动填写联盟申请表单，截图保存进度
"""

import sys
import json
import time
from pathlib import Path

# 配置文件路径
CONFIG_FILE = "affiliate_config.json"
PROGRESS_FILE = "affiliate_progress.json"

def load_config():
    """加载配置文件"""
    config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        # 创建默认配置
        default_config = {
            "user_email": "sloaris@163.com",
            "user_name": "Zhang Sir",
            "website_url": "https://sloaris1314.github.io/ai-tools-hub/",
            "linkedin_url": "https://linkedin.com/in/sloaris1314",
            "promotion_plan": "We operate an AI tools review website that publishes comprehensive reviews and tutorials for AI productivity tools. Our content targets developers, content creators, and business professionals.",
            "headless": False  # True = 无界面模式，False = 有界面模式
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        print(f"[INFO] 已创建默认配置文件: {CONFIG_FILE}")
        print(f"[INFO] 请编辑该文件填写你的信息（如果默认值不正确）")
        return default_config
    else:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def load_progress():
    """加载进度文件"""
    progress_path = Path(PROGRESS_FILE)
    if not progress_path.exists():
        return {"completed": [], "current": None}
    with open(progress_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(progress):
    """保存进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)

def apply_elevenlabs(page, config):
    """申请 ElevenLabs 联盟"""
    print("\n" + "="*60)
    print("[TASK] 开始申请 ElevenLabs 联盟")
    print("="*60)
    
    try:
        # 访问 ElevenLabs 官网
        print("[ACTION] 访问 ElevenLabs 官网...")
        page.goto("https://elevenlabs.io", timeout=30000)
        time.sleep(2)
        page.screenshot(path="screenshots/01_elevenlabs_homepage.png")
        print("[SAVE] 截图: 01_elevenlabs_homepage.png")
        
        # 查找 Affiliates 链接（通常在页面底部）
        print("[ACTION] 查找 Affiliates 页面链接...")
        
        # 尝试多种方式找到 Affiliates 链接
        affiliates_found = False
        try:
            # 方式1：直接访问已知的联盟页面
            page.goto("https://elevenlabs.io/affiliates", timeout=15000)
            affiliates_found = True
            print("[INFO] 直接访问联盟页面成功")
        except:
            # 方式2：在页面底部查找链接
            page.goto("https://elevenlabs.io", timeout=15000)
            footer = page.query_selector("footer")
            if footer:
                affiliates_link = footer.query_selector("a:text-matches('affiliate', 'i')")
                if affiliates_link:
                    affiliates_link.click()
                    affiliates_found = True
                    print("[INFO] 在页面底部找到 Affiliates 链接")
        
        if not affiliates_found:
            print("[WARN] 未找到 Affiliates 页面，请手动访问并截图")
            print("[INFO] 可能的地址: https://elevenlabs.io/affiliates")
            return False
        
        time.sleep(3)
        page.screenshot(path="screenshots/02_elevenlabs_affiliates.png")
        print("[SAVE] 截图: 02_elevenlabs_affiliates.png")
        
        # 查找 "Apply Now" 或 "Sign Up" 按钮
        print("[ACTION] 查找申请按钮...")
        apply_button = page.query_selector("text=Apply Now, text=Sign Up, text=Join")
        if apply_button:
            apply_button.click()
            print("[INFO] 点击申请按钮")
            time.sleep(3)
            page.screenshot(path="screenshots/03_elevenlabs_apply_form.png")
            print("[SAVE] 截图: 03_elevenlabs_apply_form.png")
        else:
            print("[WARN] 未找到申请按钮，可能需要先注册账号")
        
        print("\n[PAUSED] 浏览器已打开 ElevenLabs 联盟页面")
        print("[PAUSED] 请手动完成以下步骤：")
        print("  1. 填写申请表单（如需要）")
        print("  2. 提交申请")
        print("  3. 获取你的推荐链接")
        print("  4. 按 Enter 键继续...\n")
        
        input()  # 暂停，等待用户手动操作
        
        page.screenshot(path="screenshots/04_elevenlabs_after_apply.png")
        print("[SAVE] 截图: 04_elevenlabs_after_apply.png")
        
        print("\n[SUCCESS] ElevenLabs 申请流程已完成（手动部分）")
        return True
        
    except Exception as e:
        print(f"[ERROR] ElevenLabs 申请失败: {e}")
        return False

def apply_runway(page, config):
    """申请 Runway 联盟"""
    print("\n" + "="*60)
    print("[TASK] 开始申请 Runway 联盟")
    print("="*60)
    
    try:
        print("[ACTION] 访问 Runway 官网...")
        page.goto("https://runwayml.com", timeout=30000)
        time.sleep(2)
        page.screenshot(path="screenshots/05_runway_homepage.png")
        print("[SAVE] 截图: 05_runway_homepage.png")
        
        # 查找 Affiliates 页面
        print("[ACTION] 查找 Affiliates 页面...")
        try:
            page.goto("https://runwayml.com/affiliates", timeout=15000)
            print("[INFO] 直接访问联盟页面成功")
        except:
            print("[WARN] 未找到 Runway 联盟页面")
            print("[INFO] 可能需要通过 PartnerStack 申请")
        
        time.sleep(3)
        page.screenshot(path="screenshots/06_runway_affiliates.png")
        print("[SAVE] 截图: 06_runway_affiliates.png")
        
        print("\n[PAUSED] 浏览器已打开 Runway 相关页面")
        print("[PAUSED] 请手动完成申请流程")
        print("[PAUSED] 按 Enter 键继续...\n")
        
        input()
        
        print("\n[SUCCESS] Runway 申请流程已完成（手动部分）")
        return True
        
    except Exception as e:
        print(f"[ERROR] Runway 申请失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("AI 联盟申请自动化工具 v1.0")
    print("=" * 60)
    
    # 加载配置
    print("\n[INFO] 加载配置文件...")
    config = load_config()
print(f"[INFO] 用户邮箱: {config['user_email']}")
        print(f"[INFO] 网站地址: {config['website_url']}")
    
    # 创建截图目录
    screenshots_dir = Path("screenshots")
    screenshots_dir.mkdir(exist_ok=True)
    print(f"[INFO] 截图将保存到: {screenshots_dir.absolute()}")
    
    # 加载进度
    progress = load_progress()
    print(f"[INFO] 已完成: {progress['completed']}")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # 启动浏览器
            print(f"\n[INFO] 启动浏览器（headless={config['headless']}）...")
            browser = p.chromium.launch(headless=config['headless'])
            page = browser.new_page()
            print("[INFO] 浏览器启动成功")
            
            # 申请各个联盟
            tasks = [
                ("ElevenLabs", apply_elevenlabs),
                ("Runway", apply_runway),
            ]
            
            for task_name, task_func in tasks:
                if task_name not in progress['completed']:
                    print(f"\n[INFO] 开始任务: {task_name}")
                    success = task_func(page, config)
                    if success:
                        progress['completed'].append(task_name)
                        save_progress(progress)
                        print(f"[INFO] 任务 {task_name} 已完成，进度已保存")
                else:
                    print(f"\n[SKIP] 任务 {task_name} 已完成，跳过")
            
            # 关闭浏览器
            print("\n[INFO] 关闭浏览器...")
            browser.close()
            print("[INFO] 浏览器已关闭")
        
        print("\n" + "="*60)
        print("[COMPLETE] 所有任务已完成！")
        print("="*60)
        print(f"[INFO] 截图保存在: {screenshots_dir.absolute()}")
        print(f"[INFO] 进度保存在: {PROGRESS_FILE}")
        
    except Exception as e:
        print(f"\n[ERROR] 程序执行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    # 设置控制台输出编码
    sys.stdout.reconfigure(encoding='utf-8')
    
    exit_code = main()
    sys.exit(exit_code)
