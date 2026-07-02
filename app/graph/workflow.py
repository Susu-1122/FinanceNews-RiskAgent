from app.agents.news_crawler_agent import NewsCrawlerAgent
from app.agents.news_scoring_agent import NewsScoringAgent
from app.agents.report_agent import ReportAgent
from app.agents.risk_prediction_agent import RiskPredictionAgent
from app.agents.sentiment_agent import SentimentAgent
from app.schemas import ResearchReport
from app.ml.feature_engineering import build_news_features


class FinanceRiskWorkflow:
    """财经新闻风险分析工作流。"""

    def __init__(self) -> None:
        self.news_crawler = NewsCrawlerAgent()
        self.news_scorer = NewsScoringAgent()
        self.sentiment_agent = SentimentAgent()
        self.risk_prediction_agent = RiskPredictionAgent()
        self.report_agent = ReportAgent()

    def run(
        self,
        stock_name: str,
        stock_code: str = "",
        industry: str = "",
    ) -> ResearchReport:
        news, news_source_status = self.news_crawler.run(
            stock_name=stock_name,
            stock_code=stock_code,
            industry=industry,
        )

        scores = [self.news_scorer.run(item) for item in news]

        sentiment = self.sentiment_agent.run(scores)

        features = build_news_features(scores)

        risk = self.risk_prediction_agent.run(sentiment)

        report = self.report_agent.run(
            stock_name=stock_name,
            stock_code=stock_code,
            industry=industry,
            news_source_status=news_source_status,
            news=news,
            scores=scores,
            sentiment=sentiment,
            features=features,
            risk=risk,
        )

        return report