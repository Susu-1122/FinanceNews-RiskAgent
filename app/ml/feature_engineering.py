from app.schemas import NewsScore


def build_news_features(scores: list[NewsScore]) -> dict[str, float | int]:
    """将多条新闻评分聚合成机器学习特征。

    这些特征后续会作为 XGBoost 模型的输入。
    """

    if not scores:
        return {
            "news_count": 0,
            "avg_sentiment_score": 0.0,
            "min_sentiment_score": 0.0,
            "max_sentiment_score": 0.0,
            "avg_risk_score": 0.0,
            "max_risk_score": 0.0,
            "negative_news_count": 0,
            "positive_news_count": 0,
            "policy_news_count": 0,
            "competition_news_count": 0,
            "supply_chain_news_count": 0,
            "uncertainty_avg": 0.0,
            "market_attention_avg": 0.0,
        }

    sentiment_scores = [score.sentiment_score for score in scores]
    risk_scores = [score.risk_score for score in scores]
    uncertainty_scores = [score.uncertainty_score for score in scores]
    market_attention_scores = [score.market_attention for score in scores]

    return {
        "news_count": len(scores),
        "avg_sentiment_score": round(sum(sentiment_scores) / len(scores), 4),
        "min_sentiment_score": round(min(sentiment_scores), 4),
        "max_sentiment_score": round(max(sentiment_scores), 4),
        "avg_risk_score": round(sum(risk_scores) / len(scores), 4),
        "max_risk_score": round(max(risk_scores), 4),
        "negative_news_count": sum(1 for score in scores if score.sentiment_score < -0.2),
        "positive_news_count": sum(1 for score in scores if score.sentiment_score > 0.2),
        "policy_news_count": sum(1 for score in scores if score.event_type == "policy"),
        "competition_news_count": sum(1 for score in scores if score.event_type == "competition"),
        "supply_chain_news_count": sum(1 for score in scores if score.event_type == "supply_chain"),
        "uncertainty_avg": round(sum(uncertainty_scores) / len(scores), 4),
        "market_attention_avg": round(sum(market_attention_scores) / len(scores), 4),
    }