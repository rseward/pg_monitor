#!/usr/bin/env python

import unittest

from bluestone.pgmonitor.alerts import EmailAlertManager

class TestAlerts(unittest.TestCase):

    def testAlert(self):
        man = EmailAlertManager( '127.0.0.1', [ 'rseward@bluestone-consulting.com', 'sewardrobert@gmail.com' ], 'postgres@bluestone-consulting.com'  )

        man.alert( "Master Failed", "You should check it out the master failed." )

if __name__ == "__main__":
    unittest.main()
