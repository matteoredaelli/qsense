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

    def find_users_with_unpublished_apps(
        self,
        host,
        certificate,
        threshold=100,
        notify_user=False,
        mail_smtp="localhost",
        mail_subject="Qlik: too many unpublished apps",
        mail_from="noreply@localhost",
        mail_to="",
        mail_cc="",
        mail_bcc="",
    ):
        """Find users with too many unpublished apps"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        filter = "published eq False"
        ## find unpublished apps
        apps = qrs.driver.get(
            "/qrs/app/full",
            {"filter": filter},
        ).json()
        logging.debug("Found %d apps." % len(apps))
        ## extract owner IDs from apps
        users = list(map(lambda a: a["owner"]["name"] + "|" + a["owner"]["id"], apps))

        ## frequency
        users_freq = qsense.utils.count_frequency(users)
        ## filter highest values
        threshold = int(threshold)
        ##users_subset = dict(
        ##    filter(lambda elem: elem[1] > threshold, users_freq.items())
        ##)

        for u, count in users_freq.items():
            if count > threshold:
                logging.info("%s: %d" % (u, count))
                if notify_user:
                    mailto = u.split["|"][1]
                    if mail_to != "":
                        mailto = mail_to

                    notify_user_via_mail(
                        qrs,
                        mailto,
                        mail_smtp,
                        mail_subject,
                        "You have %d unpublished apps: please delete some of them!",
                        mail_from,
                        mailto,
                        mail_cc,
                        mail_bcc,
                    )

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

    def find_old_apps(
        self,
        host,
        certificate,
        modified_days=1000,
        last_reload_days=1000,
        published=False,
        target_path=".",
        save_meta=True,
        skipdata=True,
        export=False,
        delete=False,
        notify_user=False,
        mail_smtp="localhost",
        mail_subject="Your Qliksense old app is still useful?",
        mail_from="noreply@localhost",
        mail_to="",
        mail_cc="",
        mail_bcc="",
    ):
        """Find old apps using 'modified_date' and 'last_reload_time' filters:
        then you can export them or delete or notify via email the owners"""
        qrs = qsAPI.QRS(proxy=host, certificate=certificate)
        return qsense.apps.find_old_apps(
            qrs,
            modified_days,
            last_reload_days,
            published=published,
            target_path=target_path,
            save_meta=save_meta,
            skipdata=skipdata,
            export=export,
            delete=delete,
            notify_user=notify_user,
            mail_smtp=mail_smtp,
            mail_subject=mail_subject,
            mail_from=mail_from,
            mail_to=mail_to,
            mail_cc=mail_cc,
            mail_bcc=mail_bcc,
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
