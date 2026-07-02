from app.schemas import RiskPrediction, SentimentSummary


class RiskPredictionAgent:
    """风险预测 Agent。

    V0 版本使用规则生成风险概率。
    后续版本会升级为调用 XGBoost 模型。
    """

    def run(self, sentiment: SentimentSummary) -> RiskPrediction:
        risk_probability = self._calculate_risk_probability(sentiment)
        risk_level = self._get_risk_level(risk_probability)
        summary = self._build_summary(risk_probability, risk_level, sentiment)

        return RiskPrediction(
            risk_probability=risk_probability,
            risk_level=risk_level,
            summary=summary,
        )

    def _calculate_risk_probability(self, sentiment: SentimentSummary) -> float:
        base_probability = 0.3

        risk_part = sentiment.avg_risk_score * 0.45

        negative_news_part = min(sentiment.negative_news_count * 0.08, 0.24)

        if sentiment.overall_sentiment == "bearish":
            sentiment_part = 0.18
        elif sentiment.overall_sentiment == "neutral":
            sentiment_part = 0.08
        else:
            sentiment_part = -0.08

        probability = base_probability + risk_part + negative_news_part + sentiment_part
        return max(0.0, min(1.0, round(probability, 2)))

    def _get_risk_level(self, risk_probability: float) -> str:
        if risk_probability >= 0.7:
            return "high"
        if risk_probability >= 0.4:
            return "medium"
        return "low"

    def _build_summary(
        self,
        risk_probability: float,
        risk_level: str,
        sentiment: SentimentSummary,
    ) -> str:
        if risk_level == "high":
            level_text = "风险等级较高，短期需要重点关注负面新闻和事件冲击。"
        elif risk_level == "medium":
            level_text = "风险等级中等，建议持续观察后续新闻变化。"
        else:
            level_text = "风险等级较低，暂未出现明显集中风险信号。"

        return (
            f"规则模型预测风险概率为 {risk_probability}。"
            f"{level_text}"
            f"当前平均风险分为 {sentiment.avg_risk_score}，"
            f"负面新闻数量为 {sentiment.negative_news_count}。"
        )