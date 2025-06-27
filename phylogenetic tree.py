import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons

class PhylogeneticTree:
    def __init__(self):
        self.G = nx.DiGraph()
        self.G.add_node("Root")
        self.G.add_node("A")
        self.G.add_node("B")
        self.G.add_node("A1")
        self.G.add_node("A2")
        self.G.add_node("B1")
        self.G.add_node("B2")

        self.G.add_edge("Root", "A")
        self.G.add_edge("Root", "B")
        self.G.add_edge("A", "A1")
        self.G.add_edge("A", "A2")
        self.G.add_edge("B", "B1")
        self.G.add_edge("B", "B2")

        self.pos = nx.spring_layout(self.G)
        self.fig, self.ax = plt.subplots()
        self.plot_tree(self.pos)

        self.ax_spring = plt.axes([0.1, 0.05, 0.1, 0.075])
        self.spring_button = Button(self.ax_spring, 'Spring')
        self.spring_button.on_clicked(self.spring_layout)

        self.ax_circular = plt.axes([0.3, 0.05, 0.1, 0.075])
        self.circular_button = Button(self.ax_circular, 'Circular')
        self.circular_button.on_clicked(self.circular_layout)

        self.ax_random = plt.axes([0.5, 0.05, 0.1, 0.075])
        self.random_button = Button(self.ax_random, 'Random')
        self.random_button.on_clicked(self.random_layout)

        self.ax_spectral = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.spectral_button = Button(self.ax_spectral, 'Spectral')
        self.spectral_button.on_clicked(self.spectral_layout)

    def plot_tree(self, pos):
        self.ax.clear()
        nx.draw(self.G, pos, ax=self.ax, with_labels=True)
        self.ax.set_title('Phylogenetic Tree')

    def spring_layout(self, event):
        self.pos = nx.spring_layout(self.G)
        self.plot_tree(self.pos)
        self.fig.canvas.draw_idle()

    def circular_layout(self, event):
        self.pos = nx.circular_layout(self.G)
        self.plot_tree(self.pos)
        self.fig.canvas.draw_idle()

    def random_layout(self, event):
        self.pos = nx.random_layout(self.G)
        self.plot_tree(self.pos)
        self.fig.canvas.draw_idle()

    def spectral_layout(self, event):
        self.pos = nx.spectral_layout(self.G)
        self.plot_tree(self.pos)
        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()

tree = PhylogeneticTree()
tree.show()
