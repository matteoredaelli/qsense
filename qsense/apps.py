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

# import qsAPI


def extract_dataconnections_from_text(text):
    result = []
    for r in ["LIB CONNECT TO [\['](.*?)[\]']", "[\[']lib://(.*?)[\]']"]:
        reg = re.search(r, text)
        if reg:
            result = result + list(reg.groups())
    return result


def export_app(qrs, target_path, app, save_meta=True, skipdata=True):
    """Export an application to a qvd file and its definition to a json file"""
    logging.info("Exporting app: " + str(app))
    if "stream" in app and "name" in app["name"]:
        filename = app["stream"]["name"]
    else:
        filename = ""
    filename = (
        filename + "-" + app["modifiedByUserName"] + "-" + app["name"] + "-" + app["id"]
    )
    filename = re.sub("[\\\/& .]", "_", filename)
    filename = os.path.join(target_path, filename)
    if save_meta:
        with open(filename + ".json", "w") as f:
            f.write(json.dumps(app, indent=4))
    return qrs.AppExport(app["id"], filename + ".qvd", skipdata=skipdata)


def export_by_filter(
    qrs, target_path, pFilter="stream.name ne 'None'", save_meta=True, skipdata=True
):
    apps = qrs.AppGet(pFilter=pFilter)
    for app in apps:
        export_app(
            qrs,
            target_path=target_path,
            app=app,
            save_meta=save_meta,
            skipdata=skipdata,
        )
    return apps


def open_doc(qixe, qDocId):
    logging.debug(qDocId)
    return qixe.ega.open_doc(qDocId)


def get_doc(qixe, qDocId):
    logging.debug(qDocId)
    qixe.ega.open_doc(qDocId)
    time.sleep(1)
    doc = qixe.ega.get_active_doc()
    logging.debug(doc)
    return doc


def get_script(qixe, qDocId):
    doc = get_doc(qixe, qDocId)
    if "qReturn" in doc and "qHandle" in doc["qReturn"]:
        h = doc["qReturn"]["qHandle"]
        logging.debug(qixe.eaa.get_all_infos(h))
        return qixe.eaa.get_script(h)["qScript"]
    else:
        logging.error("not found or something strange appened")
        return None


def get_old_apps(qrs, modified_days, last_reload_days, published=False):
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
    logging.debug("Found {count} apps:".format(count=len(apps)))
    return apps


def find_old_apps(
    qrs,
    modified_days,
    last_reload_days,
    published,
    target_path,
    save_meta,
    skipdata,
    export,
    delete,
):
    if delete and (modified_days < 60 or last_reload_days < 60):
        logging.error("You want to delete too recent apps. Bye")
        return 1
    apps = get_old_apps(qrs, modified_days, last_reload_days, published)
    for app in apps:
        logging.debug("Found app: " + str(app))
        resp = False
        if export:
            logging.warning("Removing app: " + app["id"])
            resp = export_app(
                qrs,
                app=app,
                target_path=target_path,
                save_meta=save_meta,
                skipdata=skipdata,
            )

        if delete:
            logging.warning("Removing app: " + app["id"])
            # An app can deleted if and only if it was successuffly exported to a file
            if resp and resp.status_code == 200:
                qrs.AppDelete(app["id"])
            else:
                logging.error("Cannot export (and then delete) app: " + app["id"])
