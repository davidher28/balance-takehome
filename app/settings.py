from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """
    App Settings
    """

    app_name: str = "Balance Takehome"
    db_url: str = Field("postgresql+psycopg2://postgres:admin@db:5432", env="DB_URL")
    db_user: str = Field("postgres", env="DB_USER")
    db_password: str = Field("admin", env="DB_PASSWORD")
    db_name: str = Field("balance_db", env="DB_NAME")
    test_db_name: str = Field("test_db", env="TEST_DB_NAME")
    sandbox_company_remote_id: str = "dbf99e9f-a1ff-4396-82bc-10985fab99da"
    merge_x_account_token: str = (
        "iBcSwsx9_swa9Nj47r3VptD1sZQ_8y05K2u0DoUgNZF9CBjQYug5Yw"
    )
    merge_accounting_auth_key: str = (
        "xdyk3X0pUYxgXH0bRK2EdnH_jH9TYeizVKfi-E8AGq_jDjcDKTXqSA"
    )

    class Config:
        env_file = ".env"


settings = Settings()
