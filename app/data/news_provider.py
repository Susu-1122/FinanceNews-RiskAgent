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
                return self._deduplicate_news(rss_news), NewsSourceStatus(
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
                return self._deduplicate_news(akshare_news), NewsSourceStatus(
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

        mock_news = self._deduplicate_news(
            self._get_mock_news(stock_name, stock_code, industry)
        )
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

        for _, row in raw_news.head(settings.akshare_news_limit * 3).iterrows():
            title = self._get_first_available_value(
                row,
                ["新闻标题", "标题", "title"],
            )
            content = self._get_first_available_value(
                row,
                ["新闻内容", "内容", "content", "summary"],
            )
            url = self._get_first_available_value(
                row,
                ["新闻链接", "链接", "url", "link"],
            )
            source = self._get_first_available_value(
                row,
                ["文章来源", "来源", "source"],
            )
            published_at = self._get_first_available_value(
                row,
                ["发布时间", "时间", "date", "datetime"],
            )

            if not title:
                continue

            summary = content[:160] if content else ""
            combined_text = f"{title} {summary}"

            news_items.append(
                NewsItem(
                    title=title,
                    summary=summary,
                    content=content,
                    source=f"akshare:{source or 'unknown'}",
                    url=url,
                    published_at=published_at,
                )
            )

        keywords = [word for word in [stock_name, stock_code, industry] if word]
        filtered_news = [
            item
            for item in news_items
            if not keywords
            or any(
                keyword in f"{item.title} {item.summary} {item.content}"
                for keyword in keywords
            )
        ]

        if filtered_news:
            return filtered_news[: settings.akshare_news_limit]

        return news_items[: settings.akshare_news_limit]
    
    def _get_first_available_value(self, row, field_names: list[str]) -> str:
        for field_name in field_names:
            if field_name in row:
                value = row.get(field_name)
                if value is not None:
                    value_text = str(value).strip()
                    if value_text and value_text.lower() != "nan":
                        return value_text
        return ""

    def _deduplicate_news(self, news_items: list[NewsItem]) -> list[NewsItem]:
        seen_keys: set[str] = set()
        deduplicated: list[NewsItem] = []

        for item in news_items:
            title = item.title.strip()
            url = item.url.strip()

            if not title:
                continue

            if url:
                key = f"url::{url}"
            else:
                key = f"title::{title}"

            if key in seen_keys:
                continue

            seen_keys.add(key)
            deduplicated.append(item)

        return deduplicated

    def _fallback_to_mock(
        self,
        requested_provider: str,
        stock_name: str,
        stock_code: str,
        industry: str,
        reason: str,
    ) -> tuple[list[NewsItem], NewsSourceStatus]:
        mock_news = self._deduplicate_news(
            self._get_mock_news(stock_name, stock_code, industry)
        )
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