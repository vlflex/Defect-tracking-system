from dataclasses import dataclass

@dataclass(frozen=True)
class ServerSetting:
    IP = '127.0.0.1'