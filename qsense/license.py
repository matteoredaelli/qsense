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
"""
  license.py

  functions about license
"""

import logging
from datetime import date
from datetime import timedelta
import qsAPI

def deallocate_unused_analyzer_licenses(qrs, days, dryrun=True):
    """ deallocate_unused_analyzer_licenses """
    today = date.today()
    last_used = (today - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    logging.debug("Last used date = " + last_used)

    pFilter = "lastUsed lt '{last_used}'".format(last_used=last_used)
    logging.debug("Searching licenses with pFilter= " + str(pFilter))
    analyzers = qrs.driver.get("/qrs/license/analyzeraccesstype/full").json()
    logging.debug("Found %d Analyzer licenses" % len(analyzers))
    for u in analyzers:
        logging.warning("removing analyzer license for user %s" % u["user"]["name"])
        if not dryrun:
            qrs.driver.delete("/qrs/license/analyzeraccesstype/" + u["id"])


def deallocate_analyzer_licenses_for_professionals(qrs, dryrun=True):
    def extract_users(licenses):
        return list(map(lambda u: u["user"]["userId"], licenses))

    def extract_licenses_for_user(licenses, userId):
        return list(filter(lambda u: u["user"]["userId"] == userId, licenses))

    analyzers = qrs.driver.get("/qrs/license/analyzeraccesstype/full").json()
    logging.debug("Analyzer licenses: %d" % len(analyzers))
    analyzers_list = extract_users(analyzers)

    professionals = qrs.driver.get("/qrs/license/professionalaccesstype/full").json()
    logging.debug("Professional licenses: %d" % len(professionals))
    professionals_list = extract_users(professionals)

    to_be_removes = list(set(analyzers_list) & set(professionals_list))
    logging.warning("Licenses to be removed: %d" % len(to_be_removes))

    for u in list(
        map(lambda u: extract_licenses_for_user(analyzers, u), to_be_removes)
    ):
        assert len(u) == 1
        u = u[0]
        logging.warning("removing analyzer license for user %s" % u["user"]["name"])
        if not dryrun:
            qrs.driver.delete("/qrs/license/analyzeraccesstype/" + u["id"])
