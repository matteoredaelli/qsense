#!/usr/bin/env python3
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
import fire
import json
import qsAPI
import qsense


class Qsense:
    """qsense is a python and command line tool for Qliksense administrators"""

    def qrs_get_entity(self, host, certificate, entity, count=False, filter="1 eq 1"):
        """Get entity list or count"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        if count:
            full_or_count = "count"
        else:
            full_or_count = "full"
        result = qrs.driver.get(
            "/qrs/{entity}/{full_or_count}".format(
                entity=entity, full_or_count=full_or_count
            ),
            {"filter": filter},
        ).json()
        print(json.dumps(result))

    def deallocate_unused_analyzer_licenses(self, host, certificate, days, dryrun=True):
        """Deallocate analyzer license not used for N days"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.license.deallocate_unused_analyzer_licenses(qrs, days, dryrun)

    def deallocate_analyzer_licenses_for_professionals(
        self, host, certificate, dryrun=True
    ):
        """Deallocate analyzer license fom users with a professional license"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.license.deallocate_analyzer_licenses_for_professionals(qrs, dryrun)

    def delete_removed_exernally_users(
        self, host, certificate, user_directory, dryrun=True
    ):
        """Delete users that were removed externally (from active directory?)"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.users.delete_removed_exernally_users(qrs, user_directory, dryrun)

    def export_apps(
        self, host, certificate, target_path, filter="stream.name ne 'None'"
    ):
        """Export (published or passing any other filter) applications to qvd files"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.apps.export_by_filter(qrs, target_path=target_path, pFilter=filter)

    def export_users(self, host, certificate):
        """Export users and his/her groups"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        qsense.users.export_users_and_groups(qrs)

    def export_delete_old_apps(
        self,
        host,
        certificate,
        target_path,
        modified_days=1000,
        last_reload_days=1000,
        published=False,
        save_meta=True,
        skipdata=True,
        export=False,
        delete=False,
    ):
        """Export and delete old apps using 'modified_date' and 'last_reload_time' filters."""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        return qsense.apps.export_delete_old_apps(
            qrs,
            target_path,
            modified_days,
            last_reload_days,
            published=published,
            save_meta=save_meta,
            skipdata=skipdata,
            export=export,
            delete=delete,
        )

    def update_custom_property_with_users_list(
        self,
        host,
        certificate,
        custom_property_name,
        user_directory,
        dryrun=True,
        threshold=100,
    ):
        """update the value of a custom property with the list of all qliksense users"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        return qsense.custom_property.update_custom_property_with_users_list(
            qrs, custom_property_name, user_directory, dryrun, threshold
        )


def main():
    """main"""
    logging.basicConfig(level=logging.DEBUG)
    fire.Fire(Qsense)


if __name__ == "__main__":
    main()
