import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    """项目配置。

    所有环境变量都集中在这里读取，避免散落在各个文件中。
    """

    news_provider: str = os.getenv("NEWS_PROVIDER", "mock")
    rss_url: str = os.getenv("RSS_URL", "https://feeds.bbci.co.uk/news/business/rss.xml")
    akshare_news_limit: int = int(os.getenv("AKSHARE_NEWS_LIMIT", "10"))
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    llm_model: str = os.getenv("LLM_MODEL", "mock-model")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    xgboost_model_path: str = os.getenv(
        "XGBOOST_MODEL_PATH",
        "models/xgb_risk_model.json",
    )
    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    @property
    def has_llm_api_key(self) -> bool:
        return bool(self.llm_api_key.strip())


settings = Settings()