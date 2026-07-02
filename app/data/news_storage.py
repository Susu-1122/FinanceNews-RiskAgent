import csv
from pathlib import Path

from app.schemas import NewsItem, NewsSourceStatus


class NewsStorage:
    """新闻保存工具。

    当前版本只保存最近一次分析的新闻。
    后续可以扩展为保存历史新闻和评分。
    """

    def __init__(self, output_path: str = "data/latest_news.csv") -> None:
        self.output_path = Path(output_path)

    def save_latest_news(
        self,
        stock_name: str,
        stock_code: str,
        industry: str,
        news_source_status: NewsSourceStatus,
        news: list[NewsItem],
    ) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with self.output_path.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "stock_name",
                    "stock_code",
                    "industry",
                    "requested_provider",
                    "actual_provider",
                    "fallback_used",
                    "fallback_reason",
                    "title",
                    "summary",
                    "content",
                    "source",
                    "url",
                    "published_at",
                ],
            )
            writer.writeheader()

            for item in news:
                writer.writerow(
                    {
                        "stock_name": stock_name,
                        "stock_code": stock_code,
                        "industry": industry,
                        "requested_provider": news_source_status.requested_provider,
                        "actual_provider": news_source_status.actual_provider,
                        "fallback_used": news_source_status.fallback_used,
                        "fallback_reason": news_source_status.fallback_reason,
                        "title": item.title,
                        "summary": item.summary,
                        "content": item.content,
                        "source": item.source,
                        "url": item.url,
                        "published_at": item.published_at,
                    }
                )