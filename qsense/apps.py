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

import qsAPI
import logging
import json
import os
import re
from datetime import date
from datetime import timedelta


def export_apps(qrs, target_path, apps, save_meta=True, skipdata=True):
    for app in apps:
        logging.info("Exporting app: " + str(app))
        if "stream" in app and "name" in app["name"]:
            filename = app["stream"]["name"]
        else:
            filename = ""
        filename = (
            filename
            + "-"
            + app["modifiedByUserName"]
            + "-"
            + app["name"]
            + "-"
            + app["id"]
        )
        filename = re.sub("[\\\/& .]", "_", filename)
        filename = os.path.join(target_path, filename)
        if save_meta:
            with open(filename + ".json", "w") as f:
                f.write(json.dumps(apps, indent=4))
        qrs.AppExport(app["id"], filename + ".qvd", skipdata=skipdata)


def export_by_filter(
    qrs, target_path, pFilter="stream.name ne 'None'", save_meta=True, skipdata=True
):
    apps = qrs.AppGet(pFilter=pFilter)
    return export_apps(
        qrs, target_path=target_path, apps=apps, save_meta=save_meta, skipdata=skipdata
    )


def get_old_apps(qrs, modified_days=180, last_reload_days=180, published=False):
    today = date.today()
    modified_date = (today - timedelta(days=modified_days)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    logging.debug("Modified date = " + modified_date)

    last_reload_time = (today - timedelta(days=last_reload_days)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    logging.debug("Last reload time = " + last_reload_time)
    pFilter = "published eq {published} and modifiedDate lt '{modified}' and lastReloadTime lt '{reload}'".format(
        published=published, modified=modified_date, reload=last_reload_time
    )
    logging.debug("Search apps with pFilter= " + str(pFilter))
    apps = qrs.AppGet(pFilter=pFilter)
    ##l = map(lambda a: { key:value for key,value in a.items()
    ##                    if key in ['id', 'name',
    ##                               'createdDate',
    ##                               'modifiedDate', 'modifiedByUserName',
    ##                               'published', 'lastReloadTime', 'fileSize']}, apps)
    return apps


def export_delete_old_apps(
    qrs,
    target_path,
    modified_days,
    last_reload_days,
    published=False,
    save_meta=True,
    skipdata=True,
    export=True,
    delete=False,
):
    if delete and (modified_days < 60 or last_reload_days < 60):
        logginf.error("You want to delete too recent apps. Bye")
        return 1
    apps = get_old_apps(qrs, modified_days, last_reload_days, published)
    if export:
        export_apps(
            qrs,
            apps=apps,
            target_path=target_path,
            save_meta=save_meta,
            skipdata=skipdata,
        )
    for app in apps:
        logging.warning("Removing app: " + str(app))
        if delete:
            qrs.AppDelete(app["id"])
