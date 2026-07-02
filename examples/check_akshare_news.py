import argparse

import akshare as ak


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="检查 AkShare A 股个股新闻接口返回内容",
    )
    parser.add_argument(
        "--symbol",
        required=True,
        help="A 股股票代码，例如：300750、600519、002594",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="展示新闻条数",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print(f"正在请求 AkShare 个股新闻，股票代码：{args.symbol}")

    try:
        df = ak.stock_news_em(symbol=args.symbol)
    except Exception as exc:
        print("AkShare 请求失败：")
        print(exc)
        return

    print("")
    print("请求成功。")
    print(f"返回行数：{len(df)}")
    print("")

    print("字段列表：")
    for column in df.columns:
        print(f"- {column}")

    print("")
    print(f"前 {args.limit} 条新闻：")

    if df.empty:
        print("AkShare 返回了空数据。")
        return

    for index, row in df.head(args.limit).iterrows():
        print("")
        print(f"新闻 {index + 1}")
        for column in df.columns:
            value = row.get(column)
            print(f"{column}: {value}")


if __name__ == "__main__":
    main()