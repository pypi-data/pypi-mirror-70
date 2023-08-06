"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

__version__ = "0.0.0"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "rse"
PACKAGE_URL = "http://www.github.com/rseng/rse"
KEYWORDS = "rseng,software,research software,database,taxonomy"
DESCRIPTION = "the research software encyclopedia"
LICENSE = "LICENSE"

################################################################################
# Global requirements


INSTALL_REQUIRES = ()
DATABASE_REQUIRES = (("sqlalchemy", {"min_version": None}),)
TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)


ALL_REQUIRES = INSTALL_REQUIRES + DATABASE_REQUIRES
