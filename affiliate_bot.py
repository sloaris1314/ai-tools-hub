#!/usr/bin/env python3
"""
AI联盟自动申请机器人 v1.0
使用 Playwright 自动访问各AI工具联盟申请页面
支持: 自动填表、截图留证、断点续跑
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime

CONFIG_DIR = Path(__file__).parent / "affiliate_bot_config"
CONFIG_DIR.mkdir(exist_ok=True)
PROFILE_FILE = CONFIG_DIR / "profile.json"
STATE_FILE = CONFIG_DIR / "state.json"
SCREENSHOT_DIR = CONFIG_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

# 默认申请人信息
DEFAULT_PROFILE = {
    "name": "Zhang Sir",
    "email": "sloaris@163.com",
    "website": "https://sloaris1314.github.io/ai-tools-hub/",
    "linkedin": "https://linkedin.com/in/sloaris1314",
    "github": "https://github.com/sloaris1314",
    "audience_description": "AI tools review website targeting developers, content creators, and business professionals.",
    "promotion_plan": "In-depth AI tool reviews and tutorials, SEO-optimized content, social media promotion.",
    "monthly_traffic": "0-1000",
    "country": "China"
}

# 目标联盟列表
TARGETS = [
    {"name": "ElevenLabs", "url": "https://elevenlabs.io/affiliates", "platform": "partnerstack"},
    {"name": "Runway",    "url": "https://runwayml.com/affiliates", "platform": "direct"},
    {"name": "Suno",       "url": "https://suno.com/affiliates",    "platform": "direct"},
    {"name": "Leonardo",   "url": "https://leonardo.ai/affiliates", "platform": "direct"},
    {"name": "Cursor",     "url": "https://cursor.sh/affiliates",   "platform": "direct"},
]


async def load_profile():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_PROFILE, f, indent=2, ensure_ascii=False)
        print(f"[初始化] 已创建配置文件: {PROFILE_FILE}")
        print("[初始化] 请编辑该文件填写真实信息后重新运行")
        return None


async def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "failed": [], "last_run": None, "links": {}}


async def save_state(state):
    state["last_run"] = datetime.now().isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


async def try_fill_form(page, profile):
    """尝试自动填写表单"""
    try:
        inputs = await page.query_selector_all("input:visible, textarea:visible")
        for inp in inputs:
            inp_type = (await inp.get_attribute("type") or "").lower()
            name = (await inp.get_attribute("name") or "").lower()
            pid = (await inp.get_attribute("id") or "").lower()
            placeholder = (await inp.get_attribute("placeholder") or "").lower()
            key = f"{name}_{pid}_{placeholder}"

            if inp_type == "email" or "email" in key:
                await inp.fill(profile["email"])
                print(f"    ✍️ email: {profile['email']}")
            elif inp_type == "text" and any(k in key for k in ["name", "full"]):
                await inp.fill(profile["name"])
                print(f"    ✍️ name: {profile['name']}")
            elif any(k in key for k in ["website", "url", "site"]):
                await inp.fill(profile["website"])
                print(f"    ✍️ website: {profile['website']}")
            elif "linkedin" in key or "social" in key:
                if profile.get("linkedin"):
                    await inp.fill(profile["linkedin"])
                    print(f"    ✍️ linkedin: {profile['linkedin']}")
    except Exception as e:
        print(f"  ⚠️ 自动填表异常: {e}")


async def process_target(page, profile, target, state):
    """处理单个联盟申请"""
    name = target["name"]
    url = target["url"]
    print(f"\n{'='*50}")
    print(f"🎯 处理: {name}")
    print(f"🔗 URL: {url}")
    print(f"{'='*50}")

    try:
        await page.goto(url, timeout=30000)
        await page.wait_for_timeout(3000)

        # 截图1: 初始页面
        shot1 = SCREENSHOT_DIR / f"{name}_01_landing.png"
        await page.screenshot(path=str(shot1))
        print(f"  📸 截图1: {shot1.name}")

        # 尝试自动填表
        await try_fill_form(page, profile)

        # 截图2: 填表后
        shot2 = SCREENSHOT_DIR / f"{name}_02_filled.png"
        await page.screenshot(path=str(shot2))
        print(f"  📸 截图2: {shot2.name}")

        # 打印当前URL
        print(f"  🌐 当前URL: {page.url}")

        # 等待用户确认
        print(f"\n  ⏸️  请在浏览器中检查页面，手动完成申请（如需要）")
        link = input("  申请完成后，粘贴你的专属推荐链接（没有就直接回车）: ").strip()

        if link:
            state["links"][name] = link
            print(f"  ✅ 已记录 {name} 推荐链接")
            print(f"  🔗 {link}")

        state["completed"].append(name)
        await save_state(state)
        print(f"  ✅ {name} 处理完成")
        return True

    except Exception as e:
        print(f"  ❌ 处理 {name} 时出错: {e}")
        state["failed"].append({"name": name, "error": str(e)})
        await save_state(state)
        return False


async def main():
    print("\n" + "=" * 60)
    print("🤖 AI联盟自动申请机器人 v1.0")
    print("=" * 60)

    profile = await load_profile()
    if not profile:
        return

    print(f"\n📋 申请人: {profile['name']} <{profile['email']}>")
    print(f"🌐 网站: {profile['website']}")

    state = await load_state()
    print(f"\n📊 历史记录: 已完成{len(state['completed'])}个, 失败{len(state['failed'])}个")

    # 过滤未完成的
    remaining = [t for t in TARGETS if t["name"] not in state["completed"]]
    if not remaining:
        print("\n✅ 所有联盟均已处理完毕！")
        if state["links"]:
            print("\n📝 已获取的推荐链接:")
            for name, link in state["links"].items():
                print(f"  {name}: {link}")
        return

    print(f"\n📝 待处理: {[t['name'] for t in remaining]}")
    input("\n按 Enter 启动浏览器...")

    async with (await __import__('playwright.async_api').async_playwright()).start() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=800)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        print("\n🌐 浏览器已启动，开始处理...\n")

        for target in remaining:
            await process_target(page, profile, target, state)

        print("\n" + "=" * 60)
        print("🎉 所有任务处理完毕！")
        print("=" * 60)
        print(f"✅ 完成: {len(state['completed'])} 个")
        print(f"❌ 失败: {len(state['failed'])} 个")

        if state["links"]:
            print("\n📝 已获取的推荐链接:")
            for name, link in state["links"].items():
                print(f"  {name}: {link}")
            print(f"\n💡 提示: 链接已保存在 {STATE_FILE}")

        input("\n按 Enter 关闭浏览器...")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
