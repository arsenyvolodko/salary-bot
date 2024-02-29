from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBManager:
    def __init__(self, uri: str, db_name: str) -> None:
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db["salary"]

    async def get_sum_by_dt_range(self, start_dt: datetime, end_dt: datetime, end_dt_operator: str = "lt"):
        pipeline = [
            {
                "$match": {
                    "dt": {
                        "$gte": start_dt,
                        end_dt_operator: end_dt
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_sum": {"$sum": "$value"}
                }
            }
        ]
        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
        if result:
            return result[0]["total_sum"]
        return 0

    def close(self) -> None:
        self.client.close()
