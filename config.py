import os

class Config:
    # Required configurations
        BOT_TOKEN = os.getenv("BOT_TOKEN")
            API_ID = int(os.getenv("API_ID", 0))
                API_HASH = os.getenv("API_HASH")
                    ADMINS = [int(admin) for admin in os.getenv("ADMINS", "").split(",")]
                        DB_URI = os.getenv("DB_URI")
                            DB_NAME = os.getenv("DB_NAME", "vj_bot")
                                
                                    # Optional configurations
                                        ERROR_MESSAGE = os.getenv("ERROR_MESSAGE", "false").lower() == "true"
                                            PORT = int(os.getenv("PORT", 8080))
                                                ERROR_LOGS = os.getenv("ERROR_LOGS")  # Channel ID for error reportingreporting