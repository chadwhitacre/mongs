"""
Launch Aspen configured to host Mongs
"""

import os
from aspen import serve, website


def run():
	os.environ.update(
		ASPEN_WWW_ROOT='www',
		ASPEN_PROJECT_ROOT='.',
		ASPEN_RENDERER_DEFAULT='jinja2',
	)
	serve(website.Website())


if __name__ == '__main__':
	run()
