#!/usr/bin/env python3

import fire
import logging
import qsAPI
import pysense


def export_apps(host, certificate, targetPath, pFilter="stream.name ne 'None'"):
    qrs = qsAPI.QRS(proxy=host, certificate=certificate)
    pysense.apps.export(qrs, targetPath=targetPath, pFilter=pFilter)

def export_users(host, certificate):
    qrs = qsAPI.QRS(proxy=host, certificate=certificate)
    pysense.users.export_users_and_groups(qrs)

def export_delete_old_apps(host, certificate, target_path, modified_date='2020-08-01 00:00:00', last_reload_time='2020-08-01 00:00:00', published=False, save_meta=True, skipdata=True, export=True, delete=False):
    qrs = qsAPI.QRS(proxy=host, certificate=certificate)
    return pysense.apps.export_delete_old_apps(qrs, target_path, modified_date, last_reload_time, published=published, save_meta=save_meta, skipdata=skipdata, export=export, delete=delete)

def main():
    logging.basicConfig(level=logging.DEBUG)

    fire.Fire({
        'export_apps': export_apps,
        'export_users': export_users,
        'export_delete_old_apps': export_delete_old_apps
        })
 ##   filename = sys.argv[1]
 ##   import_file(filename)

if __name__ == "__main__":
    main()
