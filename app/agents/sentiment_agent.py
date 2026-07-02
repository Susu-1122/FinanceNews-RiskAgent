from app.schemas import NewsScore, SentimentSummary


class SentimentAgent:
    """情绪汇总 Agent。

    将多条新闻评分聚合成整体情绪结论。
    """

    def run(self, scores: list[NewsScore]) -> SentimentSummary:
        if not scores:
            return SentimentSummary(
                overall_sentiment="neutral",
                avg_sentiment_score=0.0,
                avg_risk_score=0.0,
                negative_news_count=0,
                positive_news_count=0,
                summary="没有可用于分析的新闻评分，整体情绪暂定为中性。",
            )

        avg_sentiment_score = round(
            sum(score.sentiment_score for score in scores) / len(scores),
            2,
        )
        avg_risk_score = round(
            sum(score.risk_score for score in scores) / len(scores),
            2,
        )

        negative_news_count = sum(1 for score in scores if score.sentiment_score < -0.2)
        positive_news_count = sum(1 for score in scores if score.sentiment_score > 0.2)

        if avg_sentiment_score > 0.2:
            overall_sentiment = "bullish"
            summary = "相关新闻整体偏正面，市场情绪对目标标的较为友好。"
        elif avg_sentiment_score < -0.2:
            overall_sentiment = "bearish"
            summary = "相关新闻整体偏负面，需要关注短期风险和事件冲击。"
        else:
            overall_sentiment = "neutral"
            summary = "相关新闻整体偏中性，暂未形成明显单边情绪。"

        if avg_risk_score >= 0.65:
            summary += " 同时，新闻风险分较高，建议重点关注风险事件。"
        elif avg_risk_score >= 0.45:
            summary += " 新闻风险分处于中等水平，需要持续观察。"
        else:
            summary += " 新闻风险分较低，短期风险信号不强。"

        return SentimentSummary(
            overall_sentiment=overall_sentiment,
            avg_sentiment_score=avg_sentiment_score,
            avg_risk_score=avg_risk_score,
            negative_news_count=negative_news_count,
            positive_news_count=positive_news_count,
            summary=summary,
        )