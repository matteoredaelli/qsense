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

import logging
import json
import os
import re
import time
from datetime import date
from datetime import timedelta

def find_changes(qrs, start_time, end_time, out):
    ## out can be json|text
    pFilter = f"modifiedDate ge '{start_time}' and modifiedDate le '{end_time}'"
    logging.debug("Searching dataconnections with pFilter= " + str(pFilter))
    path = "/qrs/dataconnection/full"
    param = {"filter": pFilter} 
    result = qrs.driver.get(path, param).json()
    if out == "text":
        result = map(
            lambda a: "{time}: data connection '{name}' was created/modified".format(
                time=a["modifiedDate"], name=a["name"]
            ),
            result,
        )
        result = list(result)
        result.sort()
    return result
