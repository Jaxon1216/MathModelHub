#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版 Wikipedia Pageviews 爬虫
专门为DWTS选手爬取Wikipedia页面浏览量数据

使用方法：
    python crawl_pageviews_fixed.py

输出：
    - pageviews_all_celebrities.csv：所有选手的pageviews数据
"""

import os
import re
import time
import random
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List

import pandas as pd
import requests

# ==================== 配置 ====================
class Config:
    # 输入输出
    official_csv = "2026_MCM_Problem_C_Data.csv"
    manual_map_csv = "manual_celebrity_wiki_map.csv"  # 手动映射表
    output_dir = "external_outputs"
    output_file = "pageviews_all_celebrities.csv"
    
    # HTTP配置
    user_agent = "DWTS-MCM-Crawler/2.0 (Educational research project)"
    timeout_sec = 30
    max_retries = 3
    
    # 爬取配置
    sleep_base = 1.0  # 基础等待时间（秒）
    sleep_jitter = 0.5  # 随机抖动
    
    # Pageviews API配置
    pageviews_project = "en.wikipedia"
    pageviews_access = "all-access"
    pageviews_agent = "user"
    
    # 每个赛季的大致时间范围（DWTS通常在秋季播出）
    # 格式：season -> (start_month, start_year, end_month, end_year)
    # 如果不确定，使用整年数据
    season_dates = {
        1: ("2005-06-01", "2005-07-31"),
        2: ("2006-01-01", "2006-03-31"),
        3: ("2006-09-01", "2006-11-30"),
        4: ("2007-03-01", "2007-05-31"),
        5: ("2007-09-01", "2007-11-30"),
        6: ("2008-03-01", "2008-05-31"),
        7: ("2008-09-01", "2008-11-30"),
        8: ("2009-03-01", "2009-05-31"),
        9: ("2009-09-01", "2009-11-30"),
        10: ("2010-03-01", "2010-05-31"),
        11: ("2010-09-01", "2010-11-30"),
        12: ("2011-03-01", "2011-05-31"),
        13: ("2011-09-01", "2011-11-30"),
        14: ("2012-03-01", "2012-05-31"),
        15: ("2012-09-01", "2012-11-30"),
        16: ("2013-03-01", "2013-05-31"),
        17: ("2013-09-01", "2013-11-30"),
        18: ("2014-03-01", "2014-05-31"),
        19: ("2014-09-01", "2014-11-30"),
        20: ("2015-03-01", "2015-05-31"),
        21: ("2015-09-01", "2015-11-30"),
        22: ("2016-03-01", "2016-05-31"),
        23: ("2016-09-01", "2016-11-30"),
        24: ("2017-03-01", "2017-05-31"),
        25: ("2017-09-01", "2017-11-30"),
        26: ("2018-03-01", "2018-05-31"),
        27: ("2018-09-01", "2018-11-30"),
        28: ("2019-09-01", "2019-11-30"),
        29: ("2020-09-01", "2020-11-30"),
        30: ("2021-09-01", "2021-11-30"),
        31: ("2022-09-01", "2022-11-30"),
        32: ("2022-09-01", "2022-11-30"),  # Disney+
        33: ("2024-09-01", "2024-11-30"),
        34: ("2024-09-01", "2024-11-30"),
    }

# ==================== 日志配置 ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ==================== HTTP工具 ====================
def make_session() -> requests.Session:
    """创建HTTP会话"""
    session = requests.Session()
    session.headers.update({"User-Agent": Config.user_agent})
    return session

def polite_sleep(extra: float = 0.0):
    """礼貌等待，避免被封"""
    time.sleep(Config.sleep_base + random.random() * Config.sleep_jitter + extra)

# ==================== Wikipedia API ====================
def search_wiki_title(session: requests.Session, name: str) -> Optional[str]:
    """
    使用Wikipedia API搜索选手对应的页面标题
    """
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": name,
        "format": "json",
        "srlimit": 5
    }
    
    for attempt in range(Config.max_retries):
        try:
            resp = session.get(api_url, params=params, timeout=Config.timeout_sec)
            resp.raise_for_status()
            data = resp.json()
            
            results = data.get("query", {}).get("search", [])
            if results:
                return results[0].get("title")
            return None
            
        except Exception as e:
            logger.warning(f"搜索失败 (尝试 {attempt+1}/{Config.max_retries}): {name}, 错误: {e}")
            polite_sleep(extra=1.0 + attempt)
    
    return None

def fetch_pageviews(session: requests.Session, wiki_title: str, 
                    start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    获取Wikipedia页面的每日浏览量
    
    API文档: https://wikimedia.org/api/rest_v1/
    
    Args:
        wiki_title: Wikipedia页面标题
        start_date: 开始日期 (YYYYMMDD)
        end_date: 结束日期 (YYYYMMDD)
    
    Returns:
        DataFrame with columns: [date, pageviews]
    """
    # URL编码标题
    article = wiki_title.replace(" ", "_")
    article_encoded = requests.utils.quote(article, safe="")
    
    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"{Config.pageviews_project}/{Config.pageviews_access}/{Config.pageviews_agent}/"
        f"{article_encoded}/daily/{start_date}/{end_date}"
    )
    
    for attempt in range(Config.max_retries):
        try:
            resp = session.get(url, timeout=Config.timeout_sec)
            
            if resp.status_code == 404:
                logger.debug(f"页面不存在: {wiki_title}")
                return None
            
            resp.raise_for_status()
            data = resp.json()
            
            items = data.get("items", [])
            if not items:
                return None
            
            df = pd.DataFrame(items)
            df["date"] = pd.to_datetime(df["timestamp"].str[:8], format="%Y%m%d")
            df = df.rename(columns={"views": "pageviews"})
            return df[["date", "pageviews"]]
            
        except Exception as e:
            logger.warning(f"Pageviews失败 (尝试 {attempt+1}/{Config.max_retries}): {wiki_title}, 错误: {e}")
            polite_sleep(extra=1.0 + attempt)
    
    return None

# ==================== 主逻辑 ====================
def load_official_data() -> pd.DataFrame:
    """加载官方数据"""
    df = pd.read_csv(Config.official_csv)
    logger.info(f"加载官方数据: {len(df)} 位选手")
    return df

def load_manual_map() -> Dict[str, str]:
    """加载手动映射表"""
    if not os.path.exists(Config.manual_map_csv):
        return {}
    
    df = pd.read_csv(Config.manual_map_csv)
    mapping = dict(zip(df["celebrity_name"], df["wiki_title"]))
    logger.info(f"加载手动映射: {len(mapping)} 条")
    return mapping

def get_season_date_range(season: int) -> tuple:
    """获取赛季的日期范围"""
    if season in Config.season_dates:
        start, end = Config.season_dates[season]
        return start.replace("-", ""), end.replace("-", "")
    else:
        # 默认使用2024年
        return "20240101", "20241231"

def crawl_all_celebrities(official_df: pd.DataFrame, manual_map: Dict[str, str]) -> pd.DataFrame:
    """
    爬取所有选手的Pageviews
    """
    session = make_session()
    results = []
    failed = []
    
    # 获取唯一的 (选手, 赛季) 组合
    celebrities = official_df[["celebrity_name", "season"]].drop_duplicates()
    total = len(celebrities)
    
    logger.info(f"开始爬取 {total} 位选手的Pageviews...")
    
    for idx, (_, row) in enumerate(celebrities.iterrows()):
        name = row["celebrity_name"]
        season = row["season"]
        
        # 进度显示
        if (idx + 1) % 20 == 0:
            logger.info(f"进度: {idx+1}/{total} ({(idx+1)/total*100:.1f}%)")
        
        # 1. 查找Wikipedia标题
        if name in manual_map:
            wiki_title = manual_map[name]
            logger.debug(f"使用手动映射: {name} -> {wiki_title}")
        else:
            wiki_title = search_wiki_title(session, name)
            polite_sleep()
        
        if not wiki_title:
            logger.warning(f"找不到Wikipedia页面: {name}")
            failed.append({"celebrity_name": name, "season": season, "error": "Wiki title not found"})
            continue
        
        # 2. 获取日期范围
        start_date, end_date = get_season_date_range(season)
        
        # 3. 爬取Pageviews
        pv_df = fetch_pageviews(session, wiki_title, start_date, end_date)
        polite_sleep()
        
        if pv_df is None or pv_df.empty:
            logger.warning(f"Pageviews为空: {name} (S{season})")
            failed.append({"celebrity_name": name, "season": season, "wiki_title": wiki_title, "error": "No pageviews data"})
            continue
        
        # 4. 计算统计量
        total_pv = pv_df["pageviews"].sum()
        avg_pv = pv_df["pageviews"].mean()
        max_pv = pv_df["pageviews"].max()
        
        results.append({
            "celebrity_name": name,
            "season": season,
            "wiki_title": wiki_title,
            "total_pageviews": total_pv,
            "avg_daily_pageviews": avg_pv,
            "max_daily_pageviews": max_pv,
            "days_with_data": len(pv_df)
        })
        
        logger.debug(f"成功: {name} (S{season}) - 总浏览量: {total_pv:,}")
    
    # 保存结果
    results_df = pd.DataFrame(results)
    failed_df = pd.DataFrame(failed)
    
    return results_df, failed_df

def main():
    """主函数"""
    os.makedirs(Config.output_dir, exist_ok=True)
    
    # 加载数据
    official_df = load_official_data()
    manual_map = load_manual_map()
    
    # 爬取
    results_df, failed_df = crawl_all_celebrities(official_df, manual_map)
    
    # 保存结果
    output_path = os.path.join(Config.output_dir, Config.output_file)
    results_df.to_csv(output_path, index=False)
    logger.info(f"✅ 保存成功: {output_path} ({len(results_df)} 条记录)")
    
    # 保存失败记录
    if len(failed_df) > 0:
        failed_path = os.path.join(Config.output_dir, "pageviews_failures.csv")
        failed_df.to_csv(failed_path, index=False)
        logger.info(f"⚠️ 失败记录: {failed_path} ({len(failed_df)} 条)")
    
    # 统计
    logger.info("=" * 50)
    logger.info(f"爬取完成!")
    logger.info(f"  成功: {len(results_df)} 位选手")
    logger.info(f"  失败: {len(failed_df)} 位选手")
    if len(results_df) > 0:
        logger.info(f"  平均浏览量: {results_df['avg_daily_pageviews'].mean():,.0f}/天")

if __name__ == "__main__":
    main()
