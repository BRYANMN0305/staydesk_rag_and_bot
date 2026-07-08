import os
from dotenv import load_dotenv

load_dotenv()


class SettingsBot:
    TOKEN_TELEGRAM_BOT: str = os.getenv("TOKEN_TELEGRAM_BOT", "")

    def validate(self):
        if not self.TOKEN_TELEGRAM_BOT:
            raise ValueError(
                "TOKEN_TELEGRAM_BOT no está configurado en el archivo .env"
            )


settingsBot = SettingsBot()
