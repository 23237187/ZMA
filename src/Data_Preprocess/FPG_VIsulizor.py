import ast
import fileinput
import pandas as pd
import seaborn as sns

class FPG_Visulizor:
    def __init__(self, rule_path):
        self.rule_path = rule_path

    def fpg_result_demo_process(self):
        df = pd.read_csv(self.rule_path, header=None, sep='conf:')
        df.columns = ['rule', 'conf']
        conf_series = df.conf
        df = pd.DataFrame(df.rule.str.split('=>', 1).tolist(), columns=['left', 'right'])
        df['conf'] = conf_series
        print(df.shape)
        df = df.sort(['conf'], ascending=False)
        df_high = df[0:21]
        df_med = df[265:286]
        df_low = df[565:586]
        sub_df = pd.concat([df_high, df_med, df_low])
        # print(sub_df)
        sub_df = sub_df.pivot(index='left', columns='right')
        sub_df.fillna(0, inplace=True)
        print(sub_df)
        print(type(sub_df.columns))
        sns.set()
        sns.heatmap(sub_df)
        sns.plt.show()


