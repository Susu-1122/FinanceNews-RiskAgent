import feedparser

from app.config import settings
from app.schemas import NewsItem, NewsSourceStatus


class NewsProvider:
    """新闻数据 Provider。

    支持 mock 和 rss 两种新闻源。
    """

    def get_news(
        self,
        stock_name: str,
        stock_code: str = "",
        industry: str = "",
    ) -> tuple[list[NewsItem], NewsSourceStatus]:
        requested_provider = settings.news_provider

        if requested_provider == "rss":
            rss_news = self._get_rss_news(stock_name, stock_code, industry)
            if rss_news:
                return rss_news, NewsSourceStatus(
                    requested_provider=requested_provider,
                    actual_provider="rss",
                    fallback_used=False,
                    fallback_reason="",
                )

            mock_news = self._get_mock_news(stock_name, stock_code, industry)
            return mock_news, NewsSourceStatus(
                requested_provider=requested_provider,
                actual_provider="mock",
                fallback_used=True,
                fallback_reason="RSS 未匹配到相关新闻，已回退到 Mock 新闻。",
            )

        mock_news = self._get_mock_news(stock_name, stock_code, industry)
        return mock_news, NewsSourceStatus(
            requested_provider=requested_provider,
            actual_provider="mock",
            fallback_used=False,
            fallback_reason="",
        )

    def _get_rss_news(
        self,
        stock_name: str,
        stock_code: str = "",
        industry: str = "",
    ) -> list[NewsItem]:
        feed = feedparser.parse(settings.rss_url)
        news_items: list[NewsItem] = []

        keywords = [
            word
            for word in [stock_name, stock_code, industry]
            if word
        ]

        for entry in feed.entries[:20]:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            published = entry.get("published", "")

            combined_text = f"{title} {summary}"

            if keywords and not any(keyword in combined_text for keyword in keywords):
                continue

            news_items.append(
                NewsItem(
                    title=title,
                    summary=summary,
                    source="rss",
                    url=link,
                    published_at=published,
                )
            )

        return news_items

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