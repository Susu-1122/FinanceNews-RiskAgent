import argparse

from app.graph.workflow import FinanceRiskWorkflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="财经新闻风险联动智能调研助手 V0",
    )

    parser.add_argument(
        "--stock-name",
        required=True,
        help="股票名称，例如：宁德时代",
    )
    parser.add_argument(
        "--stock-code",
        default="",
        help="股票代码，例如：300750",
    )
    parser.add_argument(
        "--industry",
        default="",
        help="行业名称，例如：新能源车",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    workflow = FinanceRiskWorkflow()

    report = workflow.run(
        stock_name=args.stock_name,
        stock_code=args.stock_code,
        industry=args.industry,
    )

    print(report.report_text)


if __name__ == "__main__":
    main()