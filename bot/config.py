from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    token: str
    users_ids: list[int]
    imei_api_token: str

def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        token=env.str("BOT_TOKEN"),
        users_ids=list(map(int, env.list("USERS_LIST"))),
        imei_api_token=env.str("IMEI_API_TOKEN"),
    )
