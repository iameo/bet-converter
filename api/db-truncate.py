'''
Run as a cronjob to keep database size under control

'''
import time

from api.db import bookingslips, database



safekeep_days = 2
ms_current_time = time.time()*1000
ms_one_day = 86400*1000

timestamp_reminder = int(ms_current_time - (safekeep_days*ms_one_day))


async def truncate_db():
    query = bookingslips.delete().where(bookingslips.created_at.timestamp()*1000 < timestamp_reminder)
    return await database.execute(query=query)
