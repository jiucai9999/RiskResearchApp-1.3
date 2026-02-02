import streamlit as st
from datetime import datetime
import json

from .db import init_db, get_conn
from .logic import calc_position, calc_institution_stats, load_trades

init_db()

st.set_page_config(page_title="多品种交易风控与研究系统", layout="wide")
st.title("📊 多品种交易 · 风控 & 研究系统")

INSTITUTION_POOLS = {
    "黄金": ["高盛", "瑞银", "摩根士丹利", "花旗", "摩根大通", "美银"],
    "股票": ["高盛", "瑞银", "摩根士丹利", "中金", "中信", "华泰"],
    "基金": ["易方达", "南方基金", "富国", "广发", "博时"],
    "ETF": ["高盛", "瑞银", "摩根士丹利", "中金", "中信"]
}

product = st.sidebar.selectbox("交易品类", list(INSTITUTION_POOLS.keys()))

st.subheader("🧮 下单前风控")
c1, c2 = st.columns(2)

with c1:
    account = st.number_input("账户资金", 100000.0, step=1000.0)
    risk_percent = st.number_input("单笔风险 %", 2.0, step=0.1)

with c2:
    entry = st.number_input("入场价", 100.0)
    stop = st.number_input("止损价", 95.0)
    target = st.number_input("止盈价", 120.0)

symbol = st.text_input("📌 代码", "")

inst_prices = {}
with st.expander("🏦 投资机构预期价格"):
    for inst in INSTITUTION_POOLS[product]:
        use = st.checkbox(inst, key=f"use_{inst}")
        price = st.number_input(inst, key=f"price_{inst}", disabled=not use)
        if use and price > 0:
            inst_prices[inst] = price

inst_avg, inst_median, inst_max, inst_min = calc_institution_stats(inst_prices)

if inst_avg:
    st.info(
        f"📊 均值 {inst_avg:.2f} ｜ 中位 {inst_median:.2f} ｜ "
        f"最大 {inst_max:.2f} ｜ 最小 {inst_min:.2f}"
    )

reason = st.text_area("🧠 交易理由")
emotion = st.selectbox("😐 交易情绪", ["冷静", "犹豫", "冲动", "恐惧", "自信"])

position = rr = 0.0
if st.button("✅ 计算风控"):
    position, rr = calc_position(account, risk_percent, entry, stop, target)
    st.success(f"📦 仓位 {position:.2f} ｜ 📊 盈亏比 {rr:.2f}")

result = st.number_input("本笔结果", 0.0)

if st.button("💾 保存交易"):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO trades VALUES (
            NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            product, symbol, account, risk_percent,
            entry, stop, target, position, rr, result,
            reason, emotion,
            json.dumps(inst_prices, ensure_ascii=False),
            inst_avg, inst_median, inst_max, inst_min
        )
    )
    conn.commit()
    conn.close()
    st.success("✅ 已保存")
    st.rerun()

st.divider()
df = load_trades(product)
st.dataframe(df.tail(10), use_container_width=True)

st.download_button(
    "📥 下载 CSV",
    df.to_csv(index=False, encoding="utf-8-sig"),
    "trades.csv"
)
