import numpy as np
import pandas as pd

from bokeh.plotting import figure, show, output_file


class Data_Visulizor:
    def __init__(self, cluster_centroids_path,
                 cluster_points_path,
                 cluster_radius_path,
                 cluster_prob_path):
        self.cluster_centroids_path = cluster_centroids_path
        self.cluster_points_path = cluster_points_path
        self.cluster_radius_path = cluster_radius_path
        self.cluster_prob_path = cluster_prob_path
        self.centroids_df = self.read_cluster_centroids_and_radius()
        self.points_and_prob_df = self.read_cluster_points_and_probability()

    def read_cluster_centroids_and_radius(self):
        centoids_df = pd.read_csv(self.cluster_centroids_path, header=None)
        centoids_df.columns = ["clusterID", "F1", "F2", "F3"]
        centoids_df = centoids_df.set_index(centoids_df.ix[:, "clusterID"])
        centoids_df = centoids_df.ix[:, ["F1", "F2", "F3"]]
        # print(centoids_df)
        radius_df = pd.read_csv(self.cluster_radius_path, header=None)
        radius_df.columns = ["clusterID", "RF1", "RF2", "RF3"]
        radius_df = radius_df.set_index(radius_df.ix[:, "clusterID"])
        radius_df = radius_df.ix[:, ["RF1", "RF2", "RF3"]]
        # print(radius_df)
        centoids_df = pd.concat([centoids_df, radius_df], axis=1)
        return centoids_df

    def read_cluster_points_and_probability(self):
        points_df = pd.read_csv(self.cluster_points_path, header=None)
        points_df.columns = ["F1", "F2", "F3"]
        points_df.index = range(1, 31)
        prob_df = pd.read_csv(self.cluster_prob_path, header=None)
        prob_df = prob_df.ix[1:, 1:]
        prob_df.columns = ["SV-0", "SV-2", "SV-1"]
        prob_df = prob_df[["SV-0", "SV-1", "SV-2"]]
        points_and_prob_df = pd.concat([points_df, prob_df], axis=1)

        # print(points_df)
        # print(prob_df)
        # print(points_and_prob_df)

        return points_and_prob_df

    def draw_cluster_oval(self):
        print(self.centroids_df)
        output_file("test.html")
        p = figure(width=400, height=400)
        p.oval(x=self.centroids_df.ix[:, 'F1'].tolist(),
               y=self.centroids_df.ix[:, 'F2'].tolist(),
               width=self.centroids_df.ix[:, 'RF1'].tolist(),
               height=self.centroids_df.ix[:, 'RF2'].tolist(),
               fill_color="#CAB2D6",
               fill_alpha=0.6,
               line_color="#000000",
               line_width=1)
        show(p)

    def draw_points(self):
        df = self.points_and_prob_df
        X = np.array(df['F1'].tolist())
        Y = np.array(df['F2'].tolist())
        output_file("test.html")
        radii = [0.01] * 30
        colors = ["#%02x%02x%02x" % (r, g, b)
                  for r, g, b in
                  zip(np.floor(np.array(df['SV-0'].tolist()) * 255),
                      np.floor(np.array(df['SV-1'].tolist()) * 255),
                      np.floor(np.array(df['SV-2'].tolist()) * 255))]
        print(colors)
        p = figure(width=400, height=400)
        p.scatter(X, Y,
                  radius=radii,
                  fill_color=colors,
                  fill_alpha=0.6,
                  line_color=None)
        show(p)

    def F1_F2_draw(self):
        output_file("F1_F2.html")
        p = figure(width=1000, height=600)
        max_distance = [1.9, 1.5, 1.1]
        x_range = [0.3, 0.3, 1.0]
        y_range = [0.92, 1.3, 1.1]
        p.oval(x=self.centroids_df.ix[:, 'F1'].tolist(),
               y=self.centroids_df.ix[:, 'F2'].tolist(),
               # width=np.array(self.centroids_df.ix[:, 'RF1'].tolist()) * 2,
               # height=np.array(self.centroids_df.ix[:, 'RF2'].tolist()) * 2,
               # width=np.array(max_distance),
               # height=np.array(max_distance),
               width=np.array(x_range) * 2 / 0.75,
               height=np.array(y_range) * 2 / 0.75,
               fill_color=["#FF0000", "#00FF00", "#0000FF"],
               fill_alpha=0.3,
               line_color="#000000",
               line_width=1)


        df = self.points_and_prob_df
        X = np.array(df['F1'].tolist())
        Y = np.array(df['F2'].tolist())
        radii = [0.02] * 30
        colors = ["#%02x%02x%02x" % (r, g, b)
                  for r, g, b in
                  zip(np.floor(np.array(df['SV-0'].tolist()) * 255),
                      np.floor(np.array(df['SV-1'].tolist()) * 255),
                      np.floor(np.array(df['SV-2'].tolist()) * 255))]
        p.scatter(X, Y,
                  radius=radii,
                  fill_color=colors,
                  fill_alpha=1.0,
                  line_color=None)


        show(p)

    def F2_F3_draw(self):
        output_file("F2_F3.html")
        p = figure(width=1000, height=600)
        max_distance = [1.9, 1.5, 1.1]
        x_range = [0.92, 1.1, 1.5]
        y_range = [1.7, 1.3, 1.1]
        p.oval(x=self.centroids_df.ix[:, 'F2'].tolist(),
               y=self.centroids_df.ix[:, 'F3'].tolist(),
               # width=np.array(self.centroids_df.ix[:, 'RF2'].tolist()) * 2 /0.75,
               # height=np.array(self.centroids_df.ix[:, 'RF3'].tolist()) * 2 /0.75,
               # width=np.array(max_distance),
               # height=np.array(max_distance),
               width=np.array(x_range) * 2 / 0.75,
               height=np.array(y_range) * 2 / 0.75,
               fill_color=["#FF0000", "#00FF00", "#0000FF"],
               fill_alpha=0.3,
               line_color="#000000",
               line_width=1)


        df = self.points_and_prob_df
        X = np.array(df['F2'].tolist())
        Y = np.array(df['F3'].tolist())
        radii = [0.03] * 30
        colors = ["#%02x%02x%02x" % (r, g, b)
                  for r, g, b in
                  zip(np.floor(np.array(df['SV-0'].tolist()) * 255),
                      np.floor(np.array(df['SV-1'].tolist()) * 255),
                      np.floor(np.array(df['SV-2'].tolist()) * 255))]
        p.scatter(X, Y,
                  radius=radii,
                  fill_color=colors,
                  fill_alpha=1.0,
                  line_color=None)


        show(p)

    def F1_F3_draw(self):
        output_file("F1_F3.html")
        p = figure(width=1000, height=600)
        max_distance = [1.9, 1.5, 1.1]
        x_range = [0.3, 0.3, 1.0]
        y_range = [1.7, 1.3, 1.1]
        p.oval(x=self.centroids_df.ix[:, 'F1'].tolist(),
               y=self.centroids_df.ix[:, 'F3'].tolist(),
               # width=np.array(self.centroids_df.ix[:, 'RF2'].tolist()) * 2 /0.75,
               # height=np.array(self.centroids_df.ix[:, 'RF3'].tolist()) * 2 /0.75,
               # width=np.array(max_distance),
               # height=np.array(max_distance),
               width=np.array(x_range) * 2 / 0.75,
               height=np.array(y_range) * 2 / 0.75,
               fill_color=["#FF0000", "#00FF00", "#0000FF"],
               fill_alpha=0.3,
               line_color="#000000",
               line_width=1)


        df = self.points_and_prob_df
        X = np.array(df['F1'].tolist())
        Y = np.array(df['F3'].tolist())
        radii = [0.02] * 30
        colors = ["#%02x%02x%02x" % (r, g, b)
                  for r, g, b in
                  zip(np.floor(np.array(df['SV-0'].tolist()) * 255),
                      np.floor(np.array(df['SV-1'].tolist()) * 255),
                      np.floor(np.array(df['SV-2'].tolist()) * 255))]
        p.scatter(X, Y,
                  radius=radii,
                  fill_color=colors,
                  fill_alpha=1.0,
                  line_color=None)


        show(p)



