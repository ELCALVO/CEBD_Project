import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 5
class AppFctComp5(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_5.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_5, "")
        try:
            cursor = self.data.cursor()
            requete = """SELECT numEq,avg(ageSp) as ageMoy
                        FROM LesSportifs JOIN LesEquipiers LE on LesSportifs.numSp = LE.numSp
                        WHERE numEq IN (SELECT numIn
                                        FROM lesResultats R
                                        JOIN LesInscriptions I on R.gold = I.numIN)
                        GROUP BY numEq
            """
            result = cursor.execute(requete)
        except Exception as e:
            self.ui.table_fct_comp_5.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_5, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_5, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_5, "Aucun résultat")