from app.schemas import (
    NewsItem,
    NewsScore,
    ResearchReport,
    RiskPrediction,
    SentimentSummary,
)


class ReportAgent:
    """报告生成 Agent。"""

    def run(
        self,
        stock_name: str,
        stock_code: str,
        industry: str,
        news: list[NewsItem],
        scores: list[NewsScore],
        sentiment: SentimentSummary,
        risk: RiskPrediction,
    ) -> ResearchReport:
        report_text = self._build_report_text(
            stock_name=stock_name,
            stock_code=stock_code,
            industry=industry,
            news=news,
            scores=scores,
            sentiment=sentiment,
            risk=risk,
        )

        return ResearchReport(
            stock_name=stock_name,
            stock_code=stock_code,
            industry=industry,
            news=news,
            scores=scores,
            sentiment=sentiment,
            risk=risk,
            report_text=report_text,
        )

    def _build_report_text(
        self,
        stock_name: str,
        stock_code: str,
        industry: str,
        news: list[NewsItem],
        scores: list[NewsScore],
        sentiment: SentimentSummary,
        risk: RiskPrediction,
    ) -> str:
        lines = []

        lines.append(f"# {stock_name} 财经新闻风险调研报告")
        lines.append("")
        lines.append("## 一、核心结论")
        lines.append(f"- 股票名称：{stock_name}")
        lines.append(f"- 股票代码：{stock_code or '未提供'}")
        lines.append(f"- 所属行业：{industry or '未提供'}")
        lines.append(f"- 综合风险等级：{risk.risk_level}")
        lines.append(f"- 风险概率：{risk.risk_probability}")
        lines.append(f"- 整体新闻情绪：{sentiment.overall_sentiment}")
        lines.append("")

        lines.append("## 二、情绪与风险概览")
        lines.append(f"- 平均情绪分：{sentiment.avg_sentiment_score}")
        lines.append(f"- 平均风险分：{sentiment.avg_risk_score}")
        lines.append(f"- 正面新闻数量：{sentiment.positive_news_count}")
        lines.append(f"- 负面新闻数量：{sentiment.negative_news_count}")
        lines.append(f"- 情绪总结：{sentiment.summary}")
        lines.append(f"- 风险预测说明：{risk.summary}")
        lines.append("")

        lines.append("## 三、关键新闻与评分")
        for index, (item, score) in enumerate(zip(news, scores), start=1):
            lines.append(f"### 新闻 {index}")
            lines.append(f"- 标题：{item.title}")
            lines.append(f"- 摘要：{item.summary}")
            lines.append(f"- 来源：{item.source}")
            lines.append(f"- 发布时间：{item.published_at or '未知'}")
            lines.append(f"- 情绪分：{score.sentiment_score}")
            lines.append(f"- 风险分：{score.risk_score}")
            lines.append(f"- 事件类型：{score.event_type}")
            lines.append(f"- 评分理由：{score.reason}")
            lines.append("")

        lines.append("## 四、后续观察重点")
        lines.append("- 继续观察相关新闻数量是否明显增加。")
        lines.append("- 关注负面新闻是否集中在政策、竞争、成本或业绩方面。")
        lines.append("- 后续版本将接入真实新闻源、大模型评分和 XGBoost 风险预测。")
        lines.append("")

        lines.append("## 五、免责声明")
        lines.append("本报告仅用于学习、研究和系统演示，不构成任何投资建议。")

        return "\n".join(lines)