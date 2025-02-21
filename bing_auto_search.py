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
    # 使用浏览器访问必应搜索页面（关键点1：URL构造）
    driver.get(f"https://cn.bing.com/search?q={keyword}")
    time.sleep(2)  # 固定等待2秒（关键点2：页面加载等待）
    
    try:
        # 关键点3：CSS选择器定位元素
        first_result = driver.find_element(
            By.CSS_SELECTOR, 
            'li.b_algo h2 a'  # 匹配包含搜索结果的列表项中的标题链接
        )
        # 关键点4：文本处理（分割获取主名称）
        return first_result.text.split(' - ')[0]  
    except:
        return "未找到"  # 异常处理（关键点5）

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