#!/bin/sh

DOMAIN='video.converter'

/Users/alberto/Develop/py_po2mo/bin/i18ndude rebuild-pot --pot ${DOMAIN}.pot --create ${DOMAIN} ..
#i18ndude merge --pot ${DOMAIN}.pot --merge ${DOMAIN}-manual.pot
/Users/alberto/Develop/py_po2mo/bin/i18ndude sync --pot ${DOMAIN}.pot ./*/LC_MESSAGES/${DOMAIN}.po
