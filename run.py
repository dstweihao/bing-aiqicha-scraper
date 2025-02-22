from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# 配置参数
with open("keywords.txt", "r") as f:
    search_keywords = [line.strip() for line in f.readlines()]
output_file = "企业名称清单.xlsx"
USE_AIQICHA = False  # 模式切换开关：True=仅爱企查结果，False=普通模式

def bing_search(keyword):
    # 动态构建查询URL
    query = f"{keyword}+site%3Aaiqicha.baidu.com" if USE_AIQICHA else keyword
    driver.get(f"https://cn.bing.com/search?q={query}")
    time.sleep(2)
    
    try:
        # 根据模式选择元素定位器
        selector = 'li.b_algo h2 a[href*="aiqicha.baidu.com"]' if USE_AIQICHA else 'li.b_algo h2 a'
        result = driver.find_element(By.CSS_SELECTOR, selector)
        
        # 统一清理企业名称
        clean_name = result.text.split(' - 爱企查')[0].split('【')[0].strip()
        return clean_name, "爱企查" if USE_AIQICHA else "普通结果"
        
    except Exception as e:
        if not USE_AIQICHA:
            # 普通模式降级处理：尝试获取第一个结果
            try:
                fallback = driver.find_element(By.CSS_SELECTOR, 'li.b_algo h2 a')
                return fallback.text.split(' - ')[0].strip(), "普通结果（待确认）"
            except:
                return keyword, "未找到"
        return keyword, "未找到（爱企查）"

# 启动浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 批量处理（修改结果记录部分）
results = []
for kw in search_keywords:
    name, source = bing_search(kw)
    results.append({
        "关键词": kw, 
        "企业全称": name,
        "来源": source  # 新增来源标识列
    })
    print(f"[{source}] {kw} -> {name}")

# 保存结果（增加列排序）
pd.DataFrame(results)[["关键词", "企业全称", "来源"]].to_excel(output_file, index=False)
driver.quit()