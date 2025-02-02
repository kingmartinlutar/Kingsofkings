from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

class Database:
    def __init__(self):
            self.client = None
                    self.db = None
                            self.users = None

                                async def initialize(self):
                                        self.client = AsyncIOMotorClient(Config.DB_URI)
                                                self.db = self.client[Config.DB_NAME]
                                                        self.users = UserManager(self.db.users)
                                                                
                                                                        # Create indexes
                                                                                await self.db.users.create_index("user_id", unique=True)

                                                                                class UserManager:
                                                                                    def __init__(self, collection):
                                                                                            self.collection = collection

                                                                                                async def get_user(self, user_id: int):
                                                                                                        return await self.collection.find_one({"user_id": user_id})

                                                                                                            async def update_session(self, user_id: int, session: str):
                                                                                                                    await self.collection.update_one(
                                                                                                                                {"user_id": user_id},
                                                                                                                                            {"$set": {"session": session}},
                                                                                                                                                        upsert=True
                                                                                                                                                                )

                                                                                                                                                                # Global database instance
                                                                                                                                                                db = Database()Database()Database()Database()