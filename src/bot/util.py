import json
from datetime import datetime

import config
from src.consts import *
from src.db.ManagerDB import MongoDBManager

db_manager = MongoDBManager(config.DB_URI, config.DB_NAME)


async def get_time_from_string(time_string: str) -> datetime:
    return datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%S")


async def get_data_from_message(text: str) -> dict[str, datetime | AggregationType]:
    dates = re.findall(DATE_REG_PATTERN, text)
    group_type = re.findall(TYPE_REG_PATTERN, text)
    return {"dt_from": await get_time_from_string(dates[0]),
            "dt_upto": await get_time_from_string(dates[1]),
            "group_type": AGGREGATION_TYPE_BY_STRING[group_type[0]]}


async def validate_message(text: str) -> bool:
    res = re.fullmatch(QUERY_REG_PATTERN, text)
    if not res:
        return False
    return True


async def construct_response(**kwargs) -> str:
    return str(json.dumps(kwargs))


async def get_values_by_dt_range(dt_from: datetime,
                                 dt_upto: datetime,
                                 group_type: AggregationType) -> dict[str, list[int | str]]:
    cur_start = dt_from
    cur_end = dt_from + TIME_DELTA_BY_AGGREGATION_TYPE[group_type]
    sums = []
    labels = []
    while cur_start <= dt_upto:
        sums.append(await db_manager.get_sum_by_dt_range(cur_start, cur_end if cur_end < dt_upto else dt_upto,
                                                         "$lt" if cur_end < dt_upto else "$lte"))
        labels.append(cur_start.strftime("%Y-%m-%dT%H:%M:%S"))
        cur_start = cur_end
        cur_end = cur_end + TIME_DELTA_BY_AGGREGATION_TYPE[group_type]
    return {
        "dataset": sums,
        "labels": labels
    }
