# FinanceNews-RiskAgent

财经新闻风险联动智能调研助手。

本项目目标是构建一个 AI Agent，用于自动采集指定股票或行业的财经新闻，调用大模型进行多维度情感与风险评分，并结合 XGBoost 模型输出短期风险预测和中文调研报告。

> 当前版本为 V0，主要用于跑通完整流程。当前新闻数据为 Mock 数据，风险预测为规则模型，不构成任何投资建议。

## 一、项目功能

用户输入股票名称、股票代码和行业后，系统自动完成：

1. 生成模拟财经新闻
2. 对每条新闻进行情绪和风险评分
3. 汇总整体新闻情绪
4. 生成规则版风险概率和风险等级
5. 输出中文调研报告
6. 通过网页展示分析结果
7. 通过 FastAPI 提供 JSON 接口

## 二、当前版本

当前 V0 版本已完成：

- Mock 新闻采集 Agent
- 新闻评分 Agent
- 情绪汇总 Agent
- 风险预测 Agent
- 报告生成 Agent
- 命令行运行入口
- FastAPI 接口
- 简单网页页面
- GitHub 代码托管

暂未完成：

- 真实财经新闻爬取
- 大模型 API 评分
- XGBoost 模型训练
- XGBoost 风险预测
- 数据库存储
- 定时任务和预警

## 三、项目结构

```text
FinanceNews-RiskAgent/
  app/
    agents/
      news_crawler_agent.py
      news_scoring_agent.py
      sentiment_agent.py
      risk_prediction_agent.py
      report_agent.py
    graph/
      workflow.py
    config.py
    schemas.py
  web/
    static/
      index.html
  data/
  models/
  tests/
  main.py
  web_app.py
  requirements.txt
  README.md
  .env.example
  .gitignore