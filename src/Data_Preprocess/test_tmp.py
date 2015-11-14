
from MBA_Preparetor import *

mbp = MBA_Preparetor("/home/yang/Data_Test/sample_next", "/home/yang/Data_Test/sample_next/json")
mbp.convert_legacy_dataset_to_batch_input_file_for_mba()

# mbp = MBA_Preparetor("/home/yang/Data_Test/sample_3", "/home/yang/Data_Test/sample_3/json")
# mbp.convert_legacy_dataset_to_batch_input_file_for_mba()