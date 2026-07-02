from app.data.news_provider import NewsProvider
from app.schemas import NewsItem


class NewsCrawlerAgent:
    """新闻采集 Agent。

    Agent 负责调用新闻 Provider，不直接关心数据来自 mock、RSS 还是 API。
    """

    def __init__(self) -> None:
        self.news_provider = NewsProvider()

    def run(
        self,
        stock_name: str,
        stock_code: str = "",
        industry: str = "",
    ) -> list[NewsItem]:
        return self.news_provider.get_news(
            stock_name=stock_name,
            stock_code=stock_code,
            industry=industry,
        )