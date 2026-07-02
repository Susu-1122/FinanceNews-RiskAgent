from app.schemas import NewsItem


class NewsCrawlerAgent:
    """新闻采集 Agent。

    V0 版本先使用 Mock 新闻，后续再升级为真实新闻源。
    """

    def run(self, stock_name: str, stock_code: str = "", industry: str = "") -> list[NewsItem]:
        news = [
            NewsItem(
                title=f"{stock_name}所处行业竞争加剧，市场关注价格压力",
                summary=f"近期{industry or '相关行业'}竞争有所升温，市场担心企业利润率受到影响。",
                source="mock",
                published_at="2026-07-01",
            ),
            NewsItem(
                title=f"{stock_name}发布新产品计划，机构关注长期增长空间",
                summary="公司新产品计划受到部分机构关注，市场认为可能改善中长期增长预期。",
                source="mock",
                published_at="2026-07-01",
            ),
            NewsItem(
                title=f"{industry or stock_name}产业链出现成本波动，短期不确定性上升",
                summary="上游原材料价格波动加大，可能影响相关企业短期盈利稳定性。",
                source="mock",
                published_at="2026-07-01",
            ),
        ]

        return news