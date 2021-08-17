# qSense

*qsense* is a python library and command line tool for QLIK QlikSense. It contains some useful functions for administrators/developers of QLiksense

It uses the python library [qsAPI](https://github.com/rafael-sanz/qsAPI) for connecting to the QLiksense Repository APIs

# Installation

pip install qsense

# Usage

Look at USAGE.txt file or the source file qsense/command_line.py for details.

# Examples

## Changing all data connections after a file server migration

```bash
JSONFILE=ds-shares.json
rm $JSONFILE

qsense get_entity qlikserver.redaelli.org client.pem dataconnection --filter "connectionstring sw '\\\\\\\amzn'" | jq '.' > $JSONFILE

sed  -e 's/amznfsx94rgsb1e/amznfsxe9chyjel/g' ${JSONFILE} > new-${JSONFILE}

qsense update_entity qlikserver.redaelli.org client.pem dataconnection new-${JSONFILE}
```
