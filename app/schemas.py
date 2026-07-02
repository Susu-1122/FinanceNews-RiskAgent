from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    """一条财经新闻。"""

    title: str = Field(description="新闻标题")
    summary: str = Field(default="", description="新闻摘要")
    content: str = Field(default="", description="新闻正文")
    source: str = Field(default="mock", description="新闻来源")
    url: str = Field(default="", description="新闻链接")
    published_at: str = Field(default="", description="发布时间")


class NewsScore(BaseModel):
    """大模型或规则系统对一条新闻的多维度评分。"""

    sentiment_score: float = Field(description="情绪分数，范围 -1 到 1，越高越正面")
    risk_score: float = Field(description="风险分数，范围 0 到 1，越高风险越高")
    policy_impact: float = Field(description="政策影响，范围 -1 到 1")
    industry_impact: float = Field(description="行业影响，范围 -1 到 1")
    company_impact: float = Field(description="公司影响，范围 -1 到 1")
    market_attention: float = Field(description="市场关注度，范围 0 到 1")
    uncertainty_score: float = Field(description="不确定性分数，范围 0 到 1")
    event_type: str = Field(description="事件类型，例如 policy、competition、earnings")
    reason: str = Field(description="评分理由")

class NewsSourceStatus(BaseModel):
    """新闻源状态。"""

    requested_provider: str = Field(description="用户配置请求的新闻源")
    actual_provider: str = Field(description="实际使用的新闻源")
    fallback_used: bool = Field(description="是否发生回退")
    fallback_reason: str = Field(default="", description="回退原因")

class SentimentSummary(BaseModel):
    """多条新闻聚合后的情绪总结。"""

    overall_sentiment: str = Field(description="整体情绪：bullish、neutral、bearish")
    avg_sentiment_score: float = Field(description="平均情绪分")
    avg_risk_score: float = Field(description="平均风险分")
    negative_news_count: int = Field(description="负面新闻数量")
    positive_news_count: int = Field(description="正面新闻数量")
    summary: str = Field(description="情绪总结")


class RiskPrediction(BaseModel):
    """XGBoost 或规则模型输出的风险预测。"""

    
    risk_probability: float = Field(description="风险概率，范围 0 到 1")
    risk_level: str = Field(description="风险等级：low、medium、high")
    summary: str = Field(description="风险预测说明")


class ResearchReport(BaseModel):
    """最终输出给用户的调研报告。"""

    stock_name: str = Field(description="股票名称")
    stock_code: str = Field(default="", description="股票代码")
    industry: str = Field(default="", description="行业")
    news_source_status: NewsSourceStatus = Field(description="新闻源状态")
    news: list[NewsItem] = Field(description="相关新闻列表")
    scores: list[NewsScore] = Field(description="新闻评分列表")
    sentiment: SentimentSummary = Field(description="情绪汇总")
    features: dict[str, float | int] = Field(description="新闻聚合后的机器学习特征")
    risk: RiskPrediction = Field(description="风险预测")
    report_text: str = Field(description="中文调研报告正文")