import qsAPI
import logging
import json
import os

def export_apps(qrs, target_path, apps, save_meta=True, skipdata=True):
    for app in apps:
        logging.info("Exporting app: " + str(app))
        filename = os.path.join(target_path,  app['id'])
        if save_meta:
            with open(filename + ".json", "w") as f:
                f.write(json.dumps(apps, indent=4))
        qrs.AppExport(app['id'],  filename + ".qvd", skipdata=skipdata)

def export_by_filter(qrs, target_path, pFilter="stream.name ne 'None'", save_meta=True, skipdata=True):
    apps = qrs.AppGet(pFilter=pFilter)
    return export_apps(qrs, target_path=target_path, apps=apps, save_meta=save_meta, skipdata=skipdata)

def get_old_apps(qrs, modified_date='2020-08-01 00:00:00', last_reload_time='2020-08-01 00:00:00', published=False):
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


def export_delete_old_apps(qrs, target_path, modified_date, last_reload_time, published=False, save_meta=True, skipdata=True, export=True, delete=False):
    apps = get_old_apps(qrs, modified_date, last_reload_time, published)
    if export:
        export_apps(qrs, apps=apps, target_path=target_path, save_meta=save_meta, skipdata=skipdata)
    if delete:
        logging.warning("Removing app: " + str(app))
        qrs.AppDelete(app['id'])
