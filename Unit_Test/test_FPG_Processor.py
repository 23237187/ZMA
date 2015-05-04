__author__ = 'root'

import pprint

from FPG_Processor import *
fpg = FPG_Processor("/ZTE_Demo/FPG_result/result.txt", "/ZTE_Demo/FPG_result/fpg_result.txt")
rules = fpg.run_generate_rule()
pprint.pprint(rules)
# pprint.pprint(supportData)
