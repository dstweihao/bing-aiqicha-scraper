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
    # 访问必应搜索页（参数已编码）
    driver.get(f"https://cn.bing.com/search?q={keyword}")  # 1. 构造搜索URL
    time.sleep(2)  # 2. 固定等待页面加载
    
    try:
        # 3. 定位搜索结果元素
        first_result = driver.find_element(  # 4. 获取首个结果
            By.CSS_SELECTOR, 
            'li.b_algo h2 a'  # 匹配必应标准搜索结果结构
        )
        # 5. 清理企业名称
        return first_result.text.split(' - ')[0]  # 分割副标题
    except:
        return "未找到"  # 6. 异常处理

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