
from datetime import datetime
import fileinput
import pandas as pd
import re
import os
import glob


class MBA_Preparetor:

    def __init__(self, records_path, output_path):
        self.records_path = records_path
        self.output_path = output_path



    def convert_legacy_dataset_to_batch_input_file_for_mba(self):
        target_file_path = self.output_path + '/batch_input.txt'
        os.makedirs(self.output_path, exist_ok=True)

        for uid in range(1, 31):
            usr_records_dir = self.records_path + "/" + str(uid)
            filename_list = next(os.walk(usr_records_dir))[2]
            for filename in filename_list:
                input_file_path = usr_records_dir + '/' + filename
                output_file_path = self.output_path + '/' + str(uid) + '_' + filename
                self.specific_usr_and_date_records_2_json_format(input_file_path, output_file_path)


        # with open(target_file_path, 'a') as output_file:
        #     json_filename_list = next(os.walk(self.output_path))[2]
        #     for json_filename in json_filename_list:
        #         for line in fileinput.input(self.output_path + '/' + json_filename):
        #             print(line, file=output_file)

        read_files = glob.glob(self.output_path + '/*')
        with open(target_file_path, 'a') as outfile:
            for f in read_files:
                with open(f, "r") as infile:
                    outfile.write(infile.read())


    def specific_usr_and_date_records_2_json_format(self, records_file_path, output_path):
        df = pd.DataFrame()
        # output_json_file = records_file_path +
        for line in fileinput.input(records_file_path, inplace=True):
            print(line.replace('-|-|', ','), end='')
        df = pd.read_csv(records_file_path, header=None)
        for line in fileinput.input(records_file_path, inplace=True):
            print(line.replace(',', '-|-|'), end='')
        df.columns = ['eventTime', 'latitude', 'altitude', 'entityId', 'targetEntityId', 'event']
        df['eventTime'] = df['eventTime'].apply(self.unixtimestamp_2_ISO_8601)
        df['event'] = df['event'].apply(str)
        df['entityId'] = df['entityId'].apply(str)
        df['entityType'] = "user"
        df['targetEntityType'] = "app"
        columns_order = ['event', 'entityType', 'entityId', 'targetEntityType', 'targetEntityId', 'latitude', 'altitude', 'eventTime']
        df = df[columns_order]
        df.to_json(output_path, orient="records")
        json_fileinput = fileinput.input(output_path, inplace=True)
        first_line = json_fileinput.readline()
        print(first_line[1:], end='')
        json_fileinput.close()
        for line in fileinput.input(output_path, inplace=True):
            line = re.sub(r"}.", "}\n", line)
            line = line.replace("\"latitude\":\"null\",\"altitude\":\"null\"", "\"properties\":{\"latitude\":\"null\",\"altitude\":\"null\"}")
            print(line, end='')




    # def

    def unixtimestamp_2_ISO_8601(self, unixtimestamp):
        dt = datetime.fromtimestamp(unixtimestamp / 1000).replace(microsecond=0).isoformat()
        return dt
