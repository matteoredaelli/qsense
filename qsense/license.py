import qsAPI
import re
import logging

def deallocate_analyzer_licenses_for_professionals(qrs, dryrun=True):
    def extract_users(licenses):
        return list(map(lambda u: u["user"]["userId"], licenses))
    def extract_licenses_for_user(licenses, userId):
        return list(filter(lambda u: u["user"]["userId"] == userId, licenses))

    analyzers = qrs.driver.get('/qrs/license/analyzeraccesstype/full').json()
    logging.debug("Analyzer licenses: %d" % len(analyzers))
    analyzers_list = extract_users(analyzers)

    professionals = qrs.driver.get('/qrs/license/professionalaccesstype/full').json()
    logging.debug("Professional licenses: %d" % len(professionals))
    professionals_list = extract_users(professionals)

    to_be_removes = list(set(analyzers_list) & set(professionals_list) )
    logging.warning("Licenses to be removed: %d" % len(to_be_removes))

    for u in list(map(lambda u: extract_licenses_for_user(analyzers, u), to_be_removes)):
        assert len(u) == 1
        u = u[0]
        logging.warning("removing analyzer license for user %s" % u["user"]["name"])
        if not dryrun:
            qrs.driver.delete('/qrs/license/analyzeraccesstype/' + u["id"])
