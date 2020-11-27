
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4.ui", self)
        self.data = data
        self.refreshCatList()
        self.refreshNbEqList()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        # TODO 1.7 : fonction à modifier pour que l'équipe ne propose que des valeurs possibles pour le pays choisi
        display.refreshLabel(self.ui.label_fct_comp_4, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numSp, nomSp, prenomSp, categorieSp, dateNaisSp FROM LesSportifs_base JOIN LesEquipiers USING (numSp) WHERE pays = ? AND numEq=?",
                [self.ui.comboBox_fct_4_pays.currentText(), self.ui.comboBox_fct_4_equipe.currentText()]
            )
        except Exception as e:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_4, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")

    # Fonction de mise à jour des pays
    @pyqtSlot()
    def refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT pays FROM LesSportifs_base ORDER BY pays")
        except Exception as e:
            self.ui.comboBox_fct_4_pays.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4_pays, result)
    def refreshNbEqList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT numEq from lesEquipiers WHERE numSP in(SELECT numSP from lesSportifs_base WHERE pays=?) ORDER BY numEq",
                                    [self.ui.comboBox_fct_4_pays.currentText()])
            # ça marche aussi result = cursor.execute("SELECT DISTINCT numEq FROM lesSportifs S JOIN lesEquipiers E on(E.numSp=S.numSp) WHERE pays=? GROUP BY numEq",[self.ui.comboBox_fct_4_pays.currentText()])
        except Exception as e:
            self.ui.comboBox_fct_4_equipe.clear()
        else:
            i = display.refreshGenericCombo(self.ui.comboBox_fct_4_equipe, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_3, "Aucun résultat")
