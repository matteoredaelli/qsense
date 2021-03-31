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
import smtplib


def send_mail(mail_smtp, mail_from, mail_to, subject, msg, mail_cc, mail_bcc):
    """TODO: bcc does not work"""
    message = """From: %s>
To: %s
Cc: %s
Bcc: %s
MIME-Version: 1.0
Content-type: text/plain
Subject: %s

%s
""" % (
        mail_from,
        mail_to,
        mail_cc,
        mail_bcc,
        subject,
        msg,
    )

    try:
        server = smtplib.SMTP(mail_smtp)
        server.set_debuglevel(1)
        logging.debug("sending email to %s" % str(mail_to))
        server.sendmail(mail_from, mail_to, message)
        return server.quit()
    except Exception:
        logging.error("Error: unable to send email: %s" % message)
