import os

class Config:
    # Required configurations
        BOT_TOKEN = os.getenv("8056263089:AAHMI88zp5GyHzeaQS82BKNzGFzEI_5DAPs")
            API_ID = int(os.getenv("5969730414", 0))
                API_HASH = os.getenv("bff60a5f566d9a54c175b0001ba9615b")
                    ADMINS = [int(admin) for admin in os.getenv("ADMINS", "5969730414").split(",")]
                        DB_URI = os.getenv("mongodb+srv://lelouchlightlevi:gZRinZeJNXI55Va0@cluster0.n99js.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
                            DB_NAME = os.getenv("DB_NAME", "king_bot")
                                
                                    # Optional configurations
                                        ERROR_MESSAGE = os.getenv("ERROR_MESSAGE", "false").lower() == "true"
                                            PORT = int(os.getenv("PORT", 8080))
                                                ERROR_LOGS = os.getenv("ERROR_LOGS")  # Channel ID for error reportingreporting
