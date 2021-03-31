# qSense

*qsense* is a python library and command line tool for QLIK QlikSense. It contains some useful functions for administrators/developers of QLiksense

It uses the python library [qsAPI](https://github.com/rafael-sanz/qsAPI) for connecting to the QLiksense Repository APIs

# Installation

pip install qsense

# Usage

Look at the file qsense/command_line.py for details

## Generic Entity (app,user,dataconnection,custompropertydefinition,..)

Get all users

	qsense  qrs_get_entity qliksense.redaelli.org ~/certificates/client.pem user

Count all apps using a filter

	qsense  qrs_get_entity qliksense.redaelli.org ~/certificates/client.pem custompropertydefinition --full_or_count count --filter "name eq 'GroupAccess'"

	qsense  qrs_get_entity qliksense.redaelli.org ~/certificates/client.pem app --full_or_count count --filter "published ne True"

### Apps

#### export_apps

Export (published or passing any other filter) applications to qvd files

	qsense export_apps qliksense.redaelli.org ~/certificates/client.pem  --target_path '/tmp' --filter "published eq true"

#### find_users_with_unpublished_apps

Find users with too many unpublished apps in their work area

	qsense find_users_with_unpublished_apps qliksense.redaelli.org ~/certificates/client.pem --threshold 50

#### find_old_apps

Find old apps using 'modified_date' and 'last_reload_time' filters. Then you can export them or delete or notify via email the owners

	qsense find_old_apps qliksense.redaelli.org ~/certificates/client.pem  --target_path '/tmp' --modified_days=300 --last_reload_days=300


	qsense find_old_apps qliksense.redaelli.org ~/certificates/client.pem  --modified_days=300 --last_reload_days=300 --mail_subject "qlik - you have an old app, please delete it" --mail_to matteo@example.com

### Custom properties

#### update_custom_property_with_users_list

Update the value of a custom property (usually "UserAccess") with the list of all qliksense users.

	qsense update_custom_property_with_users_list qliksense.redaelli.org ~/certificates/client.pem UserAccess GROUP --nodryrun

### Licenses

#### deallocate_unused_analyzer_licenses

Deallocate not used (by N days) analyzer licenses

	qsense deallocate_unused_analyzer_licenses qliksense.redaelli.org ~/certificates/client.pem --nodryrun

#### deallocate_analyzer_licenses_for_professionals

Deallocate analyzer license fom users with a professional license

	qsense deallocate_analyzer_licenses_for_professionals qliksense.redaelli.org ~/certificates/client.pem --nodryrun

###  Users

#### delete_removed_exernally_users

Delete users that were removed externally (from active directory?)

	qsense delete_removed_exernally_users qliksense.redaelli.org ~/certificates/client.pem GROUP --nodryrun
