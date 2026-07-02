from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.graph.workflow import FinanceRiskWorkflow

app = FastAPI(
    title="FinanceNews-RiskAgent",
    description="财经新闻风险联动智能调研助手 V0",
    version="0.1.0",
)

app.mount("/static", StaticFiles(directory="web/static"), name="static")

workflow = FinanceRiskWorkflow()


@app.get("/")
def home() -> FileResponse:
    return FileResponse("web/static/index.html")


@app.get("/analyze")
def analyze(
    stock_name: str = Query(..., description="股票名称，例如：宁德时代"),
    stock_code: str = Query(default="", description="股票代码，例如：300750"),
    industry: str = Query(default="", description="行业名称，例如：新能源车"),
) -> dict:
    report = workflow.run(
        stock_name=stock_name,
        stock_code=stock_code,
        industry=industry,
    )

    return report.model_dump()