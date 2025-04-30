import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ファンド名リスト（新順番）
fund_order = [
    "全世界株式",
    "先進国株式",
    "米国株式_S&P500",
    "米国総合債券ファンド",
    "国内株式_TOPIX",
    "国内株式_日経平均",
    "変動国債",
    "ゴールドファンド"
]

# デフォルトのファンド設定（初期投資＆リターン・リスク定義）
default_funds = [
    {"name": "全世界株式",         "initial": 0,    "monthly": 100000,      "mean": 0.052,  "std": 0.16},
    {"name": "先進国株式",         "initial": 0,     "monthly": 0,      "mean": 0.051,  "std": 0.16},
    {"name": "米国株式_S&P500",    "initial": 0,   "monthly": 0,  "mean": 0.070,  "std": 0.20},
    {"name": "米国総合債券ファンド", "initial": 0,      "monthly": 0,    "mean": 0.025,  "std": 0.05},
    {"name": "国内株式_TOPIX",     "initial": 0,    "monthly": 0,      "mean": 0.050,  "std": 0.16},
    {"name": "国内株式_日経平均",  "initial": 0,   "monthly": 0,  "mean": 0.050,  "std": 0.16},
    {"name": "変動国債",            "initial": 0,    "monthly": 0,      "mean": 0.0083, "std": 0.02},
    {"name": "ゴールドファンド",    "initial": 0,        "monthly": 0,   "mean": 0.040,  "std": 0.12},
]

presets = {
    "Conservative（保守型）": [10000, 5000, 5000, 50000, 10000, 10000, 15000, 0],
    "Balanced（バランス型）":  [30000, 10000, 10000, 20000, 10000, 10000, 5000, 5000],
    "Aggressive（積極型）":    [35000, 15000, 25000, 0,     10000, 10000, 0,     5000],
}


correlation_matrix = np.array([
    [ 1.00, 0.98, 0.90, -0.18, 0.65, 0.60, -0.05, -0.25],
    [ 0.98, 1.00, 0.92, -0.08, 0.68, 0.68, -0.06, -0.18],
    [ 0.90, 0.92, 1.00, -0.06, 0.65, 0.60, -0.05, -0.25],
    [-0.18,-0.08,-0.06,  1.00,-0.05,-0.05,  0.05,  0.60],
    [ 0.65, 0.68, 0.65, -0.05, 1.00, 0.85,  0.00, -0.10],
    [ 0.60, 0.68, 0.60, -0.05, 0.85, 1.00,  0.00, -0.10],
    [-0.05,-0.06,-0.05,  0.05, 0.00, 0.00,  1.00,  0.10],
    [-0.25,-0.18,-0.25,  0.60,-0.10,-0.10,  0.10,  1.00],
])

def simulate_montecarlo(fund_settings, correlation_matrix, n_simulation=20000, years=20):
    np.random.seed(42)
    months = years * 12
    init_amounts = np.array([f['initial'] for f in fund_settings])
    monthly_amounts = np.array([f['monthly'] for f in fund_settings])
    mean_returns_annual = np.array([f['mean'] for f in fund_settings])
    std_devs_annual = np.array([f['std'] for f in fund_settings])
    mean_returns_monthly = mean_returns_annual / 12
    std_devs_monthly = std_devs_annual / np.sqrt(12)
    cov_matrix = np.diag(std_devs_monthly) @ correlation_matrix @ np.diag(std_devs_monthly)
    total = np.tile(init_amounts, (n_simulation, 1))
    total_history = []
    for month in range(months):
        returns = np.random.multivariate_normal(mean_returns_monthly, cov_matrix, size=n_simulation)
        total = (total + monthly_amounts) * (1 + returns)
        if (month + 1) % 12 == 0:
            total_history.append(np.sum(total, axis=1))
    return np.array(total_history)

def main():
    st.set_page_config(page_title="つみたてシミュレーション", layout="wide")
    st.title("つみたてシミュレーション")

    # ── サイドバー：シミュレーション設定 ──
    st.sidebar.header("シミュレーション設定")
    n_simulation = st.sidebar.slider("シミュレーション回数", 20000, 60000, 20000, step=5000)
    n_years = st.sidebar.number_input("運用年数（年）", min_value=1, max_value=50, value=20)
    run_simulation = st.sidebar.button("🚀 シミュレーション実行")

    # ── サイドバー：プリセット選択 ──
    st.sidebar.header("月額積立プリセット")
    preset_name = st.sidebar.selectbox(
        "プリセットを選択",
        list(presets.keys()),
        index=1  # デフォルトで Balanced を選ぶ場合は index=1
    )
    monthly_presets = presets[preset_name]
    # ── プリセット選択部分の解説 ──
    # ユーザーがプリセットを選ぶと、monthly_presets に各ファンドの月額積立額リストが入る

    # ── サイドバー：ファンド設定 ──
    st.sidebar.header("ファンド設定")
    fund_settings = []
    for i, default in enumerate(default_funds):
        with st.sidebar.expander(default["name"], expanded=False):
            # 初期投資額は固定デフォルト、プリセットには含めない
            initial = st.number_input(
                f"{default['name']}：初期投資額",
                min_value=0,
                value=default['initial'],
                step=1000,
                key=f"init_{i}"
            )
            # 月額積立額はプリセット初期値を反映
            monthly = st.number_input(
                f"{default['name']}：月額積立額",
                min_value=0,
                value=monthly_presets[i],
                step=1000,
                key=f"monthly_{i}"
            )
            mean_percent = st.number_input(
                f"{default['name']}：期待リターン（年率％）",
                value=default['mean'] * 100,
                step=0.1,
                format="%.2f",
                key=f"mean_{i}"
            )
            std_percent = st.number_input(
                f"{default['name']}：リスク（年率％）",
                value=default['std'] * 100,
                step=0.1,
                format="%.2f",
                key=f"std_{i}"
            )
            fund_settings.append({
                "name": default["name"],
                "initial": initial,
                "monthly": monthly,
                "mean": mean_percent / 100,
                "std": std_percent / 100
            })

    if run_simulation:
        # （以下は既存のシミュレーション → 結果表示ロジックと同じ）
        result = simulate_montecarlo(fund_settings, correlation_matrix, n_simulation=n_simulation, years=n_years)
        years = np.arange(1, n_years + 1)
        df_result = pd.DataFrame(result.T, columns=[f"{y}年目" for y in years])
        df_result["最終資産"] = df_result.iloc[:, -1]

        initial_sum = sum(f["initial"] for f in fund_settings)
        monthly_sum = sum(f["monthly"] for f in fund_settings)
        total_principal = initial_sum + (monthly_sum * 12 * n_years)

        risk_free_rate = 0.083/100
        returns_annual = (df_result["最終資産"] / total_principal) ** (1 / n_years) - 1
        mean_return = returns_annual.mean()
        std_return = returns_annual.std()
        sharpe_ratio = (mean_return - risk_free_rate) / std_return
        broken_rate = (df_result["最終資産"] < total_principal).mean() * 100

        df_funds = pd.DataFrame(fund_settings)
        df_funds["期待リターン（％）"] = df_funds["mean"] * 100
        df_funds["リスク（％）"] = df_funds["std"] * 100
        df_funds = df_funds.drop(columns=["mean", "std"]).rename(columns={
            "name": "ファンド名",
            "initial": "初期投資額",
            "monthly": "月額積立額"
        })

        tab1, tab2, tab3, tab4 = st.tabs(["総合指標", "資産推移", "損益ヒストグラム", "ファンド設定一覧"])

        with tab1:
            st.subheader("総合指標")
            col1, col2, col3 = st.columns(3)
            col1.metric(f"シャープレシオ (RF={risk_free_rate*100:.3f}%)", f"{sharpe_ratio:.2f}")
            col2.metric("最終資産中央値", f"{df_result['最終資産'].median():,.0f} 円")
            col3.metric("元本割れ確率", f"{broken_rate:.2f} %")
            st.write(f"期待年率リターン：{mean_return * 100:.2f} %")
            st.write(f"リターン標準偏差（リスク）：{std_return * 100:.2f} %")

        with tab2:
            st.subheader("平均・中央値資産推移")
            mean_total = df_result.iloc[:, :-1].mean()
            median_total = df_result.iloc[:, :-1].median()
            fig = px.line(x=years, y=mean_total, labels={"x": "年", "y": "平均資産"}, title="平均資産推移", color="green")
            fig.add_scatter(x=years, y=median_total, mode="lines+markers", name="中央値", color="red")
            st.plotly_chart(fig, use_container_width=True)

        with tab3:
            st.subheader(f"{n_years}年後 損益分布")
            profit = df_result["最終資産"] - total_principal
            lower = np.percentile(profit, 0)
            upper = np.percentile(profit, 99)
            mean_profit = profit.mean()
            median_profit = profit.median()
            hist, bin_edges = np.histogram(profit, bins=500, range=(lower, upper))
            mode_profit = (bin_edges[np.argmax(hist)] + bin_edges[np.argmax(hist) + 1]) / 2
            mean_profit_pct = (mean_profit / total_principal) * 100
            median_profit_pct = (median_profit / total_principal) * 100
            mode_profit_pct = (mode_profit / total_principal) * 100

            fig_profit = px.histogram(x=profit, nbins=500, labels={"x": "損益 (円)"}, title="損益ヒストグラム")
            fig_profit.update_traces(histnorm="percent")
            fig_profit.update_layout(yaxis_title="確率（%）", xaxis_range=[lower, upper])
            fig_profit.add_vline(x=mean_profit, line_dash="dash", annotation_text="平均", annotation_position="top right", color="green")
            fig_profit.add_vline(x=median_profit, line_dash="dot", annotation_text="中央値", annotation_position="top left", color="red")
            fig_profit.add_vline(x=mode_profit, line_dash="solid", annotation_text="最頻値", annotation_position="top left", color="blue")
            st.plotly_chart(fig_profit, use_container_width=True)

            st.markdown(f"""
            #### 含み損益まとめ
            - 平均損益：{mean_profit:,.0f} 円（{mean_profit_pct:+.2f}%）
            - 中央値損益：{median_profit:,.0f} 円（{median_profit_pct:+.2f}%）
            - 最頻値損益：{mode_profit:,.0f} 円（{mode_profit_pct:+.2f}%）
            """)

        with tab4:
            st.subheader("現状のファンド設定")
            st.dataframe(df_funds.style.format({
                "初期投資額": "{:,.0f} 円",
                "月額積立額": "{:,.0f} 円",
                "期待リターン（％）": "{:.2f}",
                "リスク（％）": "{:.2f}"
            }), use_container_width=True)

            st.subheader("資産クラス間の相関係数")
            df_corr = pd.DataFrame(correlation_matrix, index=fund_order, columns=fund_order)
            mask = np.triu(np.ones(df_corr.shape)).astype(bool)
            df_corr_masked = df_corr.mask(mask)
            st.dataframe(df_corr_masked.style.format("{:.2f}"), use_container_width=True)

if __name__ == "__main__":
    main()

