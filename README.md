# qsense

```
	   ____
  __ _/ ___|  ___ _ __  ___  ___
 / _` \___ \ / _ \ '_ \/ __|/ _ \
| (_| |___) |  __/ | | \__ \  __/
 \__, |____/ \___|_| |_|___/\___|
	|_|
```

*qsense* is an useful library and command line for qliksense

## Installation

pip install qsense

## Commands

### Apps

#### export_remove_old_apps

qsense export_delete_old_apps qliksense.redaelli.org ~/certificates/client.pem  --target_path '/tmp' --modified_days=300 --last_reload_days=300

### Licenses

#### deallocate_analyzer_licenses_for_professionals

qsense deallocate_analyzer_licenses_for_professionals qliksense.redaelli.org ~/certificates/client.pem --nodryrun

###  Users

#### delete_removed_exernally_users

qsense delete_removed_exernally_users qliksense.redaelli.org ~/certificates/client.pem GROUP --nodryrun
