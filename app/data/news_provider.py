import feedparser

from app.config import settings
from app.schemas import NewsItem, NewsSourceStatus


class NewsProvider:
    """新闻数据 Provider。

    支持 mock、rss、akshare 三种新闻源。
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

            return self._fallback_to_mock(
                requested_provider=requested_provider,
                stock_name=stock_name,
                stock_code=stock_code,
                industry=industry,
                reason="RSS 未匹配到相关新闻，已回退到 Mock 新闻。",
            )

        if requested_provider == "akshare":
            try:
                akshare_news = self._get_akshare_news(stock_name, stock_code, industry)
            except Exception as exc:
                return self._fallback_to_mock(
                    requested_provider=requested_provider,
                    stock_name=stock_name,
                    stock_code=stock_code,
                    industry=industry,
                    reason=f"AkShare 新闻获取失败，已回退到 Mock 新闻。错误：{exc}",
                )

            if akshare_news:
                return akshare_news, NewsSourceStatus(
                    requested_provider=requested_provider,
                    actual_provider="akshare",
                    fallback_used=False,
                    fallback_reason="",
                )

            return self._fallback_to_mock(
                requested_provider=requested_provider,
                stock_name=stock_name,
                stock_code=stock_code,
                industry=industry,
                reason="AkShare 未返回相关新闻，已回退到 Mock 新闻。",
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

        keywords = [word for word in [stock_name, stock_code, industry] if word]

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

    def _get_akshare_news(
        self,
        stock_name: str,
        stock_code: str = "",
        industry: str = "",
    ) -> list[NewsItem]:
        import akshare as ak

        if not stock_code:
            return []

        raw_news = ak.stock_news_em(symbol=stock_code)
        news_items: list[NewsItem] = []

        for _, row in raw_news.head(settings.akshare_news_limit).iterrows():
            title = str(row.get("新闻标题", "") or row.get("标题", ""))
            content = str(row.get("新闻内容", "") or row.get("内容", ""))
            url = str(row.get("新闻链接", "") or row.get("链接", ""))
            source = str(row.get("文章来源", "") or row.get("来源", "akshare"))
            published_at = str(row.get("发布时间", "") or row.get("时间", ""))

            summary = content[:120] if content else ""

            news_items.append(
                NewsItem(
                    title=title,
                    summary=summary,
                    content=content,
                    source=f"akshare:{source}",
                    url=url,
                    published_at=published_at,
                )
            )

        return news_items

    def _fallback_to_mock(
        self,
        requested_provider: str,
        stock_name: str,
        stock_code: str,
        industry: str,
        reason: str,
    ) -> tuple[list[NewsItem], NewsSourceStatus]:
        mock_news = self._get_mock_news(stock_name, stock_code, industry)
        return mock_news, NewsSourceStatus(
            requested_provider=requested_provider,
            actual_provider="mock",
            fallback_used=True,
            fallback_reason=reason,
        )

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