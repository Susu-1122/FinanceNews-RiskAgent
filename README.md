FinanceNews-RiskAgent
财经新闻风险联动智能调研助手。
本项目目标是构建一个 AI Agent，用于自动采集指定股票或行业的财经新闻，调用大模型进行多维度情感与风险评分，并结合 XGBoost 模型输出短期风险预测和中文调研报告。
当前项目已完成 V0，并正在完善 V1 新闻源接入版本。当前风险预测仍为规则模型，不构成任何投资建议。

一、项目功能
用户输入股票名称、股票代码和行业后，系统自动完成：
获取财经新闻
对每条新闻进行情绪和风险评分
汇总整体新闻情绪
生成规则版风险概率和风险等级
提取新闻聚合特征
输出中文调研报告
通过网页展示分析结果
通过 FastAPI 提供 JSON 接口
二、当前版本
V0 已完成
Mock 新闻采集 Agent
新闻评分 Agent
情绪汇总 Agent
风险预测 Agent
报告生成 Agent
命令行运行入口
FastAPI 接口
简单网页页面
GitHub 代码托管
Pytest 最小测试
V1 已完成
NewsProvider 新闻源层
Mock 新闻源
RSS 新闻源
AkShare A 股个股新闻源
新闻源状态提示
失败自动回退 Mock
网页展示实际新闻源
新闻去重
AkShare 字段兼容
AkShare 诊断脚本
新闻聚合特征
最近一次新闻保存到 data/latest_news.csv
暂未完成
大模型 API 评分
SQLite 历史数据存储
XGBoost 模型训练
XGBoost 风险预测
定时任务和预警
三、项目结构
FinanceNews-RiskAgent/
  app/
    agents/
      news_crawler_agent.py
      news_scoring_agent.py
      sentiment_agent.py
      risk_prediction_agent.py
      report_agent.py
    data/
      news_provider.py
      news_storage.py
    graph/
      workflow.py
    ml/
      feature_engineering.py
    config.py
    schemas.py
  examples/
    check_akshare_news.py
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
四、安装方法
进入项目目录：
cd "D:\python\FinanceNews-RiskAgent"
创建虚拟环境：
python -m venv .venv
激活虚拟环境：
.\.venv\Scripts\activate
如果 PowerShell 提示禁止运行脚本，可以临时执行：
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
然后再次激活：
.\.venv\Scripts\activate
安装依赖：
pip install -r requirements.txt
五、命令行运行
python main.py --stock-name 宁德时代 --stock-code 300750 --industry 新能源车
python main.py --stock-name 贵州茅台 --stock-code 600519 --industry 白酒
运行后会在终端输出 Markdown 格式的中文调研报告。
六、网页运行
启动 FastAPI 服务：
uvicorn web_app:app --reload --port 8000
浏览器打开：
http://127.0.0.1:8000
FastAPI 自动接口文档：
http://127.0.0.1:8000/docs
接口示例：
http://127.0.0.1:8000/analyze?stock_name=宁德时代&stock_code=300750&industry=新能源车
七、新闻源配置说明
当前项目支持三种新闻源。
1. Mock 新闻源
NEWS_PROVIDER=mock
Mock 新闻源使用项目内置的模拟新闻，不需要联网，也不需要任何 API Key。
适合：
测试项目是否能正常运行
没有网络时开发
避免真实新闻接口不稳定影响调试
2. RSS 新闻源
NEWS_PROVIDER=rss
RSS_URL=https://feeds.bbci.co.uk/news/business/rss.xml
RSS 新闻源会从指定的 RSS 地址读取新闻。
如果 RSS 新闻里没有匹配到你输入的股票名称、股票代码或行业关键词，系统会自动回退到 Mock 新闻。
3. AkShare 新闻源
NEWS_PROVIDER=akshare
AKSHARE_NEWS_LIMIT=10
AkShare 新闻源用于获取 A 股个股新闻。
运行示例：
python main.py --stock-name 宁德时代 --stock-code 300750 --industry 新能源车
也可以测试贵州茅台：
python main.py --stock-name 贵州茅台 --stock-code 600519 --industry 白酒
如果 AkShare 请求失败、网络不可用、接口返回为空，系统会自动回退到 Mock 新闻，并在网页和报告中显示回退原因。
八、AkShare 诊断脚本
如果你想检查 AkShare 是否正常返回新闻，可以运行：
python examples\check_akshare_news.py --symbol 300750 --limit 3
或：
python examples\check_akshare_news.py --symbol 600519 --limit 3
脚本会输出：
返回行数
字段列表
前几条新闻内容
九、新闻数据保存说明
每次运行分析后，系统会把最近一次获取到的新闻保存到：
data/latest_news.csv
这个 CSV 文件包含：
股票名称
股票代码
行业
请求新闻源
实际新闻源
是否回退
回退原因
新闻标题
新闻摘要
新闻正文
新闻来源
新闻链接
发布时间
data/*.csv 已经加入 .gitignore，所以 data/latest_news.csv 不会上传到 GitHub。
十、Agent 工作流
当前工作流：
用户输入股票信息
  ↓
NewsCrawlerAgent 调用 NewsProvider 获取新闻
  ↓
NewsScoringAgent 对新闻打分
  ↓
SentimentAgent 汇总整体情绪
  ↓
FeatureEngineering 聚合新闻特征
  ↓
RiskPredictionAgent 生成规则风险预测
  ↓
ReportAgent 生成中文调研报告
十一、后续计划
V2：接入大模型
对新闻进行多维度情绪评分
输出结构化 JSON
加入事件类型识别
替换当前关键词规则评分
V3：接入 XGBoost
构造训练数据
定义风险标签
训练 XGBoost 模型
输出风险概率
V4：增强网页
展示关键新闻列表
展示风险趋势图
展示模型特征贡献
支持报告下载
V5：自动化预警
定时抓取新闻
自动生成报告
风险升高时提醒用户
十二、免责声明
本项目仅用于学习、研究和教学演示，不构成任何投资建议。金融市场有风险，任何投资决策都应独立判断并谨慎执行