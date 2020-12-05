
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction fournie 1
class AppFctGererResultats(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_gerer_resultats.ui", self)
        self.data = data
        self.refreshNumeroEpreuve()


    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        cursor = self.data.cursor()
        try:
            if self.ui.radioButton_insert.isChecked():
                cursor.execute("INSERT INTO lesResultats(numEp,gold,silver,bronze) VALUES (?,?,?,?)",
                [self.ui.comboBox_numEp.currentText(), self.ui.comboBox_gold.currentText(), self.ui.comboBox_silver.currentText(),self.ui.comboBox_bronze.currentText()])
            elif self.ui.radioButton_update.isChecked():
                cursor.execute("UPDATE lesResultats set gold=?, silver=?, bronze=? where numEp=?",
                [self.ui.comboBox_gold.currentText(), self.ui.comboBox_silver.currentText(),
                    self.ui.comboBox_bronze.currentText(), self.ui.comboBox_numEp.currentText()])
            else:
                cursor.execute("DELETE FROM lesResultats  WHERE numEp=? and gold=? and silver=? and bronze=?",
                    [self.ui.comboBox_numEp.currentText(), self.ui.comboBox_gold.currentText(),
                    self.ui.comboBox_silver.currentText(), self.ui.comboBox_bronze.currentText()])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer l'insertion/update ou deletion : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_erreur, "Operation effectué avec succès")
            self.data.commit()




    def refreshNumeroEpreuve(self):
        try:
            cursor = self.data.cursor()
            if self.ui.radioButton_insert.isChecked():
                requete = "SELECT numEp from lesEpreuves WHERE numEp NOT IN(SELECT numEp from lesResultats)"
                numeroEpreuve = cursor.execute(requete)
            else:
                requete = "SELECT numEp from lesEpreuves JOIN lesResultats using(numEp)"
                numeroEpreuve = cursor.execute(requete)
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer les resultats : " + repr(e))
        else:
            i = display.refreshGenericCombo(self.ui.comboBox_numEp, numeroEpreuve)


    def refreshNumeroEquipe(self):
            self.refreshGold()
            self.refreshSilver()
            self.refreshBronze()


    def refreshGold(self):
        try:
            cursor = self.data.cursor()
            if self.ui.radioButton_insert.isChecked():
                equipeOr = cursor.execute("SELECT numIn FROM lesInscriptions WHERE numEp=?",
                [self.ui.comboBox_numEp.currentText()])
            elif self.ui.radioButton_update.isChecked():
                equipeOr = cursor.execute("SELECT numIn FROM lesInscriptions WHERE numEp=? AND numIn<>(SELECT gold from lesResultats where numEp=?)",
                [self.ui.comboBox_numEp.currentText(), self.ui.comboBox_numEp.currentText()])
            else:
                equipeOr = cursor.execute("SELECT gold FROM lesResultats WHERE numEp=?",
                [self.ui.comboBox_numEp.currentText()])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer les places : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_gold,equipeOr)

    def refreshSilver(self):
        try:
            cursor = self.data.cursor()
            if self.ui.radioButton_insert.isChecked():
                equipeArgent = cursor.execute("SELECT numIn FROM lesInscriptions WHERE numEp=? AND numIn<>?",
                                          [self.ui.comboBox_numEp.currentText(), self.ui.comboBox_gold.currentText()])
            elif self.ui.radioButton_update.isChecked():
                equipeArgent = cursor.execute("SELECT numIn FROM lesInscriptions WHERE numEp=? AND numIn<>(SELECT silver from lesResultats where numEp=? and numIn<>?)",
                [self.ui.comboBox_numEp.currentText(), self.ui.comboBox_numEp.currentText(), self.ui.comboBox_gold.currentText()])
            else:
                equipeArgent = cursor.execute("SELECT silver FROM lesResultats WHERE numEp=?",
                                          [self.ui.comboBox_numEp.currentText()])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer les places : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_silver, equipeArgent)

    def refreshBronze(self):
        try:
            cursor = self.data.cursor()
            if self.ui.radioButton_insert.isChecked():
                equipeBronze = cursor.execute("SELECT numIn FROM lesInscriptions WHERE numEp=? AND numIn<>? AND numIn<>?",
                [self.ui.comboBox_numEp.currentText(), self.ui.comboBox_gold.currentText(), self.ui.comboBox_silver.currentText()])
            elif self.ui.radioButton_update.isChecked():
                equipeBronze = cursor.execute("SELECT numIn FROM lesInscriptions WHERE numEp=? AND numIn<>(SELECT bronze from lesResultats where numEp=? and numIn<>? and numIn<>?)",
                [self.ui.comboBox_numEp.currentText(), self.ui.comboBox_numEp.currentText(), self.ui.comboBox_gold.currentText(), self.ui.comboBox_silver.currentText()])
            else:
                equipeBronze = cursor.execute("SELECT bronze FROM lesResultats WHERE numEp=?",
                [self.ui.comboBox_numEp.currentText()])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer les places : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_bronze, equipeBronze)






