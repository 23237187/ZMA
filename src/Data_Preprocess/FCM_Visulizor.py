import numpy as np
import pandas as pd
import ast

from bokeh.plotting import figure, show, output_file

class FCM_Viasulizor:
    def __init__(self, prob_path, point_path, center_path):
        self.prob_path = prob_path
        self.point_path = point_path
        self.center_path = center_path
        self.prob_df = self.read_probs_to_df()
        self.point_df = self.read_points_to_df()
        self.center_df = self.read_center_to_df()

    def read_probs_to_df(self):
        file_path = self.prob_path
        data_list = list()
        with open(file_path, "r") as infile:
            for line in infile:
                line.strip()
                line = line.replace("(", "")
                line = line.replace(")", "")
                line.strip()
                dict_ele = line.split(sep=",")
                uid = ast.literal_eval(dict_ele[0])
                P1 = ast.literal_eval(dict_ele[1])
                P2 = ast.literal_eval(dict_ele[2])
                data_list = data_list + [(uid, P1, P2)]
        df = pd.DataFrame(data_list)
        df = df.set_index(df.ix[:,0]).ix[:,1:]
        df = df.sort_index()
        df.index.name = "usr"
        df.columns = ["P1", "P2"]
        # print(df)
        return df

    def read_points_to_df(self):
        file_path = self.point_path
        data_list = list()
        with open(file_path, "r") as infile:

            for line in infile:
                line.strip()
                line = line.replace("(", "")
                line = line.replace(")", "")
                line.strip()
                line = line.replace('[', "")
                line = line.replace("]", "")
                line.strip()
                dict_ele = line.split(sep=",")
                uid = ast.literal_eval(dict_ele[0])
                F1 = ast.literal_eval(dict_ele[1])
                F2 = ast.literal_eval(dict_ele[2])
                data_list = data_list + [(uid, F1, F2)]
        df = pd.DataFrame(data_list)
        df = df.set_index(df.ix[:,0]).ix[:,1:]
        df = df.sort_index()
        df.index.name = "usr"
        df.columns = ["F1", "F2"]
        # print(df)
        return df

    def read_center_to_df(self):
        file_path = self.center_path
        data_list = list()
        with open(file_path, "r") as infile:
            for line in infile:
                line.strip()
                line = line.replace("[", "")
                line = line.replace("]", "")
                line.strip()
                dict_ele = line.split(sep=",")
                F1 = ast.literal_eval(dict_ele[0])
                F2 = ast.literal_eval(dict_ele[1])
                data_list = data_list + [(F1, F2)]
        df = pd.DataFrame(data_list)
        df.columns = ["F1", "F2"]
        # print(df)
        return df

    def draw_points(self):
        point_df = self.point_df
        prob_df = self.prob_df
        center_df = self.center_df
        X = np.array(point_df['F1'].tolist())
        Y = np.array(point_df['F2'].tolist())
        C_X = np.array(center_df['F1'].tolist())
        C_Y = np.array(center_df['F2'].tolist())
        output_file("test_2.html")
        radii = [0.1] * 200
        colors = ["#%02x%02x%02x" % (r, g, b)
                  for r, g, b in
                  zip(np.floor(np.array(prob_df['P1'].tolist()) * 255),
                      np.floor(np.array(prob_df['P2'].tolist()) * 0),
                      np.floor(np.array(prob_df['P2'].tolist()) * 255))]
        C_colors = ["#%02x%02x%02x" % (r, g, b)
                  for r, g, b in
                  zip(np.array([0, 1]) * 255,
                      np.array([0, 0]) * 0,
                      np.array([1, 0]) * 255)]
        # print(colors)
        p = figure(width=1700, height=900)
        p.scatter(X, Y,
                  radius=radii,
                  fill_color=colors,
                  fill_alpha=0.6,
                  line_color=None)
        p.scatter(C_X, C_Y,
                  size=50,
                  fill_color=C_colors,
                  fill_alpha=0.6,
                  line_color="#000000",
                  marker="circle_x")
        show(p)
