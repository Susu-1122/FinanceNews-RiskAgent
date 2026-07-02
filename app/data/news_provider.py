from app.config import settings
from app.schemas import NewsItem


class NewsProvider:
    """新闻数据 Provider。

    当前 V1 初始版本仍然使用 mock 数据。
    后续会在这里接入 RSS、AkShare 或其他新闻源。
    """

    def get_news(
        self,
        stock_name: str,
        stock_code: str = "",
        industry: str = "",
    ) -> list[NewsItem]:
        if settings.news_provider == "mock":
            return self._get_mock_news(stock_name, stock_code, industry)

        return self._get_mock_news(stock_name, stock_code, industry)

    def _get_mock_news(
        self,
        stock_name: str,
        stock_code: str = "",
        industry: str = "",
    ) -> list[NewsItem]:
        return [
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