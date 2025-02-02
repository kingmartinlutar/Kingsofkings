from flask import Flask
from threading import Thread
from config import Config

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running 🚀"

    def run_web_server():
        app.run(
                host='0.0.0.0',
                        port=Config.PORT,
                                use_reloader=False
                                    )

                                    # Start web server in background
                                    Thread(target=run_web_server).start()start()