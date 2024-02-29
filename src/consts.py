import re
import enum
from dateutil.relativedelta import relativedelta

DATE_REG_PATTERN = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
TYPE_REG_PATTERN = r'(hour|day|week|month)'

QUERY_REG_PATTERN = (re.compile(r'^{\s*"dt_from"\s*:\s*"' +
                                '{}'.format(DATE_REG_PATTERN) + r'"\s*,\s*"dt_upto"\s*:\s*"' +
                                '{}'.format(DATE_REG_PATTERN) + r'"\s*,\s*"group_type"\s*:\s*"' +
                                '{}'.format(TYPE_REG_PATTERN) + r'"\s*' + '}$'))


class AggregationType(enum.Enum):
    HOUR = 'hour'
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'


AGGREGATION_TYPE_BY_STRING = {i.value: i for i in AggregationType}

TIME_DELTA_BY_AGGREGATION_TYPE = {
    AggregationType.HOUR: relativedelta(hours=1),
    AggregationType.DAY: relativedelta(days=1),
    AggregationType.WEEK: relativedelta(weeks=1),
    AggregationType.MONTH: relativedelta(months=1),
}
