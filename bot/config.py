from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    token: str
    users_ids: list[int]

def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        token=env.str("BOT_TOKEN"),
        users_ids=list(map(int, env.list("USERS_LIST"))),
    )
