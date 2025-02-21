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

def bing_search(keyword):
    driver.get(f"https://cn.bing.com/search?q={keyword}")
    time.sleep(2)  # 等待加载
    
    try:
        # 定位第一个企业名称（根据编号3的必应搜索结果结构）
        first_result = driver.find_element(
            By.CSS_SELECTOR, 
            'li.b_algo h2 a'
        )
        return first_result.text.split(' - ')[0]  # 提取主名称
    except:
        return "未找到"

# 启动浏览器
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 批量处理
results = []
for kw in search_keywords:
    company_name = bing_search(kw)
    results.append({"关键词": kw, "企业全称": company_name})
    print(f"已处理: {kw} -> {company_name}")

# 保存结果
pd.DataFrame(results).to_excel(output_file, index=False)
driver.quit()