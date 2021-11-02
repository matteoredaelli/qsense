# Copyright (c) 2021 Matteo Redaelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import datetime
import logging
import qsAPI


def reloadtask_count(qrs, status):
    param = {"filter": f"operational.lastExecutionResult.status eq {status}"}
    resp = qrs.driver.get(f"/qrs/reloadtask/count", param=param).json()
    return resp


def reloadtask_status(qrs, id, max_age):
    resp = qrs.driver.get(f"/qrs/reloadtask/{id}")

    result = {}
    if resp.ok:
        status = resp.json()["operational"]["lastExecutionResult"]["status"]
        result["status"] = status
        stopTimeStr = resp.json()["operational"]["lastExecutionResult"]["stopTime"]
        result["stopTime"] = stopTimeStr
        stopTime = datetime.datetime.strptime(stopTimeStr, "%Y-%m-%dT%H:%M:%S.%f%z")
        now = datetime.datetime.now(datetime.timezone.utc)
        delta = now - stopTime
        deltaMin = delta.seconds
        result["expired"] = True if deltaMin > int(max_age) else False
    else:
        logging.error(resp)
    return result
