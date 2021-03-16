#!/usr/bin/env python3

import fire
import logging
import qsAPI
import qsense

class Qsense(object):
    def deallocate_analyzer_licenses_for_professionals(self, host, certificate, dryrun=True):
        """Deallocate analyzer license fom users with a professional license"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.license.deallocate_analyzer_licenses_for_professionals(qrs, dryrun)

    def delete_removed_exernally_users(self, host, certificate, user_directory, dryrun=True):
        """Delete users that were removed externally (from active directory?)"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.users.delete_removed_exernally_users(qrs, user_directory, dryrun)

    def export_apps(self, host, certificate, target_path, pFilter="stream.name ne 'None'"):
        """Export (published or passing any other filter) applications to qvd files"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.apps.export_by_filter(qrs, target_path=target_path, pFilter=pFilter)

    def export_users(self, host, certificate):
        """Export users and his/her groups"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.users.export_users_and_groups(qrs)

    def export_delete_old_apps(self, host, certificate, target_path,
                               modified_days=180,
                               last_reload_days=180,
                               published=False,
                               save_meta=True,
                               skipdata=True,
                               export=True,
                               delete=False):
        """Export and delete old apps using 'modified_date' and 'last_reload_time' filters."""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        return qsense.apps.export_delete_old_apps(qrs, target_path, modified_days, last_reload_days, published=published, save_meta=save_meta, skipdata=skipdata, export=export, delete=delete)

def main():
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(Qsense)

if __name__ == "__main__":
    main()
