from app.schemas import NewsItem, NewsScore


class NewsScoringAgent:
    """新闻评分 Agent。

    V0 版本使用关键词规则打分。
    后续版本会升级为调用大模型进行多维度评分。
    """

    positive_words = [
        "增长",
        "改善",
        "利好",
        "突破",
        "创新",
        "回购",
        "增持",
        "盈利",
        "新产品",
        "长期增长",
    ]

    negative_words = [
        "风险",
        "下滑",
        "压力",
        "处罚",
        "亏损",
        "调查",
        "减持",
        "竞争加剧",
        "成本波动",
        "不确定性",
    ]

    policy_words = [
        "政策",
        "监管",
        "补贴",
        "关税",
        "限制",
    ]

    competition_words = [
        "竞争",
        "价格战",
        "份额",
        "对手",
    ]

    cost_words = [
        "成本",
        "原材料",
        "供应链",
    ]

    def run(self, news_item: NewsItem) -> NewsScore:
        text = f"{news_item.title} {news_item.summary}"

        positive_count = self._count_words(text, self.positive_words)
        negative_count = self._count_words(text, self.negative_words)

        sentiment_score = self._calc_sentiment_score(positive_count, negative_count)
        risk_score = self._calc_risk_score(negative_count)

        event_type = self._detect_event_type(text)

        return NewsScore(
            sentiment_score=sentiment_score,
            risk_score=risk_score,
            policy_impact=self._calc_policy_impact(text),
            industry_impact=self._calc_industry_impact(text),
            company_impact=sentiment_score,
            market_attention=0.6 if positive_count + negative_count > 0 else 0.3,
            uncertainty_score=0.7 if "不确定性" in text or "波动" in text else 0.4,
            event_type=event_type,
            reason=self._build_reason(sentiment_score, risk_score, event_type),
        )

    def _count_words(self, text: str, words: list[str]) -> int:
        return sum(1 for word in words if word in text)

    def _calc_sentiment_score(self, positive_count: int, negative_count: int) -> float:
        raw_score = (positive_count - negative_count) * 0.3
        return max(-1.0, min(1.0, round(raw_score, 2)))

    def _calc_risk_score(self, negative_count: int) -> float:
        if negative_count <= 0:
            return 0.25
        return max(0.0, min(1.0, round(0.35 + negative_count * 0.15, 2)))

    def _detect_event_type(self, text: str) -> str:
        if any(word in text for word in self.policy_words):
            return "policy"
        if any(word in text for word in self.competition_words):
            return "competition"
        if any(word in text for word in self.cost_words):
            return "supply_chain"
        return "other"

    def _calc_policy_impact(self, text: str) -> float:
        if any(word in text for word in self.policy_words):
            return -0.4
        return 0.0

    def _calc_industry_impact(self, text: str) -> float:
        if "竞争" in text or "成本" in text or "价格" in text:
            return -0.5
        if "增长" in text or "新产品" in text:
            return 0.4
        return 0.0

    def _build_reason(self, sentiment_score: float, risk_score: float, event_type: str) -> str:
        if sentiment_score < -0.2:
            tone = "新闻偏负面"
        elif sentiment_score > 0.2:
            tone = "新闻偏正面"
        else:
            tone = "新闻整体中性"

        return f"{tone}，事件类型为 {event_type}，风险分为 {risk_score}。"