# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import multiprocessing
import secrets

default_threads = multiprocessing.cpu_count() * 5

host_ip_mapping = {}
ip_ipnum_mapping = {}
service_name_mapping = {}

secretsGenerator = secrets.SystemRandom()
