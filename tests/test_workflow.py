from app.graph.workflow import FinanceRiskWorkflow


def test_workflow_can_generate_report():
    workflow = FinanceRiskWorkflow()

    report = workflow.run(
        stock_name="宁德时代",
        stock_code="300750",
        industry="新能源车",
    )

    assert report.stock_name == "宁德时代"
    assert report.stock_code == "300750"
    assert report.industry == "新能源车"

    assert len(report.news) > 0
    assert len(report.scores) == len(report.news)

    assert 0 <= report.risk.risk_probability <= 1
    assert report.risk.risk_level in ["low", "medium", "high"]

    assert "宁德时代" in report.report_text
    assert "免责声明" in report.report_text