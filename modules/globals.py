# -*- coding: utf-8 -*-

"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

import multiprocessing

from secrets import SystemRandom

default_threads: int = multiprocessing.cpu_count() * 5

host_ip_mapping: dict = {}
ip_ipnum_mapping: dict = {}
service_name_mapping: dict = {}

secretsGenerator: SystemRandom = SystemRandom()
