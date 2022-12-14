from scipy import stats
from igraph import Graph
from igraph import plot, save, color_name_to_rgba
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import random
from tabulate import tabulate

class ITutorClassificator():

    def __init__(self, static_path):
        self.list_inter = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []
        self.random_percent = 0.9345
        self.random_name = ""
        self.STATIC_PATH = static_path
        self.PATH_GRAPH_IMAGE = static_path + "/{name}-graph.png"
        self.PATH_CURVE_IMAGE = static_path + "/{name}-curve"

    def GenerateGraph(self):

        interactions = [(random.randint(1, 50), random.randint(1, 50)) for x in
                        range(50)] if self.list_inter == [] else self.list_inter

        g = Graph(interactions, directed=True)

        if self.list_names:
            g.vs["name"] = self.list_names
            g.vs["label"] = self.list_names

        self.lista_inter_adj = np.matrix(g.get_adjacency().data)
        matrix = g.get_adjacency().data
        matrix.insert(0, self.list_names)
        for index, row in enumerate(matrix[1:]):
            row.insert(0, self.list_names[index])
        print(tabulate(matrix, headers='firstrow', tablefmt='fancy_grid'))
        """
            PLOT IGRAPH
        """
        plot(
            g,
            target=self.PATH_GRAPH_IMAGE.format(name=self.random_name),
            #layout=g.layout("kk"),
            vertex_label=g.vs['name'] if self.list_names != [] else None,
            vertex_color="rgba(5%, 100%, 100%, 0%)",
            vertex_frame_color="rgba(5%, 100%, 100%, 0%)",
            #vertex_shape="circle", # circle | rectangle
            #vertex_size=35,
            #edge_width=2,
            #edge_arrow_size=1,
            bbox=(400, 400),
            margin=60
        )

        """
            MATPLOTLIB PLOT
        """
        # fig, ax = plt.subplots()
        # plot(
        #     g,
        #     target=ax,
        #     layout="kk",  # print nodes in a circular layout
        #     vertex_size=0.3,
        #     vertex_frame_color="white",
        #     vertex_color="white",
        #     vertex_label_color=["blue"]*len(g.vs["name"]),
        #     vertex_label=g.vs['name'] if self.list_names != [] else None,
        #     vertex_label_size=10.0
        # )
        # plt.savefig(self.PATH_GRAPH_IMAGE.format(name=self.random_name+"-matplotlib"))#"./itutor/static/grafos/Graph.png"


    def CreatePlotComparison(self):
        inter_mean = np.mean(self.lista_inter_adj)
        inter_std = np.std(self.lista_inter_adj)
        interacion_norm_cdf = stats.norm.cdf(self.lista_inter_adj, loc=inter_mean, scale=inter_std)
        self.teoric_sample = np.random.randint(self.lista_inter_adj.max()+1, size=self.lista_inter_adj.shape)
        teoric_norm_cdf = stats.norm.cdf(self.teoric_sample, loc=inter_mean, scale=inter_std)

        critico = lambda x: 1.35810/np.sqrt(x)

        print("Tamanho dados intera????o: ", len(self.lista_inter_adj), "Tamanho dados teoric: ", len(self.teoric_sample))
        print("Cr??tico : ", critico(len(self.lista_inter_adj)))

        inter_kstest = stats.stats.kstest(self.lista_inter_adj, cdf="norm")
        teoric_kstest = stats.stats.kstest(self.teoric_sample, cdf="norm")
        print("\n# SEM MEDIA E DESVIO PADR??O\nINTERA????O: ", inter_kstest,
              "\nTEORICA", teoric_kstest)

        self.random_percent = inter_kstest[0]

        plt.title("Interaction Curve")
        plt.plot(interacion_norm_cdf, self.lista_inter_adj, '-b')
        plt.plot(self.teoric_sample, teoric_norm_cdf, '-g')
        plt.tight_layout()
        plt.savefig(self.PATH_CURVE_IMAGE.format(name=self.random_name))#"./itutor/static/curvas/Curves-Comparison"


    def FormatData(self, data):
        list_tuple = {}
        for d in data:
            if d["starter"]["registration"] not in list_tuple:
                list_tuple[d["starter"]["registration"]] = {"name": d["starter"]["name"], "interactions": []}
                list_tuple[d["finisher"]["registration"]] = {"name": d["finisher"]["name"], "interactions": []}
            list_tuple[d["starter"]["registration"]]["interactions"].append((d["finisher"]["registration"], d["finisher"]["name"]))
        keys = list(list_tuple.keys())
        for i in list_tuple:
            for interaction in list_tuple[i]["interactions"]:
                self.list_inter.append((keys.index(i), keys.index(interaction[0])))
        self.list_names = [list_tuple[x]["name"] for x in list_tuple]

    def Reset(self):
        self.list_inter = []
        self.list_names = []
        self.lista_inter_adj = []
        self.teoric_sample = []
        self.random_name = ""

    def GenerateRandomName(self):
        for x in range(10):
            self.random_name += random.choice("qwertyuiopasdfghjkl??zxcvbnm123456789")

    def run(self):
        self.GenerateGraph()
        self.CreatePlotComparison()

def init_app(app):
  app.itutor = ITutorClassificator(app.static_folder)