import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        try:
            self._view.txt_result.controls.clear()
            self._model.buildGraph(self._view.dd_localization.value)
            nNodi, nArchi, archiOrdinati = self._model.basiGrafo()
            self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi}"))
            self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore:"))
            for a in archiOrdinati:
                self._view.txt_result.controls.append(ft.Text(f"{a[0]} <--> {a[1]}: {a[2]["weight"]}"))
        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione grafo: {ex}")
        self._view.update_page()

    def analyze_graph(self, e):
        try:
            Comp = self._model.dettagliGrafo()
            self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse sono:"))
            for n in Comp:
                res = ""
                for c in n:
                    res += f"{c},"
                self._view.txt_result.controls.append(ft.Text(f"{res} | dimensione componente: {len(n)}"))
        except Exception as ex:
            self._view.create_alert(f"Errore nella stampa dei dettagli: {ex}")
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDD(self):
        loc = self._model.getAllLocalizations()
        locDD = list(map(lambda x: ft.dropdown.Option(x), loc))
        self._view.dd_localization.options = locDD
        self._view.update_page()

