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
        filename = app['modifiedByUserName'] + "-" + app['name'] + "-" + app["id"]
        filename = re.sub("[\\\/& .]", '_', filename)
        filename = os.path.join(target_path, filename)
        if save_meta:
            with open(filename + ".json", "w") as f:
                f.write(json.dumps(apps, indent=4))
        qrs.AppExport(app['id'],  filename + ".qvd", skipdata=skipdata)

def export_by_filter(qrs, target_path, pFilter="stream.name ne 'None'", save_meta=True, skipdata=True):
    apps = qrs.AppGet(pFilter=pFilter)
    return export_apps(qrs, target_path=target_path, apps=apps, save_meta=save_meta, skipdata=skipdata)

def get_old_apps(qrs, modified_days=180, last_reload_days=180, published=False):
    today = date.today()
    modified_date = (today - timedelta(days=modified_days)).strftime("%Y-%m-%d %H:%M:%S")
    logging.debug("Modified date = " + modified_date)

    last_reload_time = (today - timedelta(days=last_reload_days)).strftime("%Y-%m-%d %H:%M:%S")
    logging.debug("Last reload time = " + last_reload_time)
    pFilter="published eq {published} and modifiedDate lt '{modified}' and lastReloadTime lt '{reload}'".format(published=published,
                                                                                                                modified=modified_date,
                                                                                                                reload=last_reload_time)
    logging.debug("Search apps with pFilter= " + str(pFilter))
    apps = qrs.AppGet(pFilter=pFilter)
    ##l = map(lambda a: { key:value for key,value in a.items()
    ##                    if key in ['id', 'name',
    ##                               'createdDate',
    ##                               'modifiedDate', 'modifiedByUserName',
    ##                               'published', 'lastReloadTime', 'fileSize']}, apps)
    return apps


def export_delete_old_apps(qrs, target_path, modified_days, last_reload_days, published=False, save_meta=True, skipdata=True, export=True, delete=False):
    if delete and (modified_days < 60 or last_reload_days < 60):
        logginf.error("You want to delete too recent apps. Bye")
        return 1
    apps = get_old_apps(qrs, modified_days, last_reload_days, published)
    if export:
        export_apps(qrs, apps=apps, target_path=target_path, save_meta=save_meta, skipdata=skipdata)
    if delete:
        logging.warning("Removing app: " + str(app))
        qrs.AppDelete(app['id'])
