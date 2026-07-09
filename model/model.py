import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._bestCammino = []

    def getAllLocalizations(self):
        return DAO.getAllLocalizations()

    def buildGraph(self, loc):
        grafo = self._grafo
        grafo.clear()
        nodes = DAO.getAllNodes(loc)
        grafo.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n.GeneID] = n

        inter = DAO.getAllInteractions()
        for i in range(len(nodes)):
            c1 = nodes[i]
            for j in range(i+1, len(nodes)):
                c2 = nodes[j]
                if c1.Chromosome == c2.Chromosome:
                    peso = c1.Chromosome
                else:
                    peso = c1.Chromosome + c2.Chromosome
                for it in inter:
                    if c1.GeneID in it and c2.GeneID in it:
                        grafo.add_edge(c1, c2, weight=peso)
                        break

    def basiGrafo(self):
        grafo = self._grafo
        nNodi = len(grafo.nodes())
        nArchi = len(grafo.edges())
        archi = grafo.edges(data=True)
        archiOrdinati = sorted(archi, key=lambda x: x[2]['weight'])
        return nNodi, nArchi, archiOrdinati

    def dettagliGrafo(self):
        grafo = self._grafo
        compConn = list(nx.connected_components(grafo))
        validComp = []
        for c in compConn:
            if len(c) > 1:
                validComp.append(c)
        OrdComp = sorted(validComp, key=lambda x: len(x), reverse=True)
        return OrdComp

    def getBestCammino(self):
        self._bestCammino = []
        for nodo in self._grafo.nodes:
            if nodo.Essential != "?":
                self._ricorsione([nodo])
        return self._bestCammino

    def _ricorsione(self, parziale):
        grafo = self._grafo
        if len(parziale) > len(self._bestCammino):
            self._bestCammino = copy.deepcopy(parziale)
        elif len(parziale) == len(self._bestCammino):
            g1 = grafo.subgraph(self._bestCammino)
            g2 = grafo.subgraph(parziale)
            compConn1 = list(nx.connected_components(g1))
            nComp1 = len(compConn1)
            compConn2 = list(nx.connected_components(g2))
            nComp2 = len(compConn2)
            if nComp1 > nComp2:
                self._bestCammino = copy.deepcopy(parziale)

        #condizioni inserimento
        ultimo = parziale[-1]
        for candidate in grafo:
            if candidate in parziale:
                continue

            if candidate.GeneId < ultimo.GeneId:
                continue

            if candidate.Essential != ultimo.Essential:
                continue


            parziale.append(candidate)
            self._ricorsione(parziale)
            parziale.pop()





