
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDate, QTime, QDateTime, Qt
from PyQt5 import uic
from datetime import date, datetime

# Classe permettant d'afficher la fonction fournie 1
class AppFctGererInscriptions(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_gerer_inscriptions.ui", self)
        self.data = data
        self.refreshInit()
    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        cursor = self.data.cursor()
        numIn = self.ui.comboBox_numIn.currentText()
        nomD = self.ui.comboBox_nomDi.currentText()
        currentNumEp = self.ui.comboBox_numEp.currentText()
        self.refreshNbSportifs()
        try:
            nomEp = self.ui.lineEdit_nomEp.text().strip()
            nbSportifsEp = self.ui.spinBox_nbSportifs.value()
            dateEp = self.ui.dateEdit.date()
            numEp = cursor.execute("SELECT max(numEp)+1 from lesEpreuves").fetchone()
            formeEp =self.ui.comboBox_formeEp.currentText()
            catEp = self.ui.comboBox_categorieEp.currentText()
            if self.ui.radioButton_insert.isChecked():
                cursor.execute("INSERT INTO lesEpreuves(numEp,nomEp,formeEp,nomDi,categorieEp,nbSportifsEp,dateEp) VALUES (?,?,?,?,?,?,?)",
                [numEp[0], nomEp, formeEp, nomD, catEp, nbSportifsEp, dateEp.toString("d/MM/yyyy")])
                cursor.execute("INSERT INTO lesInscriptions(numIn,numEp) VALUES (?,?)", [
                    numIn, numEp[0]
                ])
            else:

                cursor.execute("INSERT INTO lesInscriptions(numIn,numEp) VALUES (?,?)", [
                numIn, currentNumEp
                ])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer l'insertion : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_erreur, "Operation effectué avec succès")
            self.data.commit()
            self.refreshNumEpreuve()


    def refreshInit(self):
            self.refreshFormeEp()
            self.refreshDisciplineEp()
            self.refreshCategorieEp()
            self.refreshNbSportifs()
            self.refreshNumInscrit()
            self.refreshNumEpreuve()

    def refreshFormeEp(self):
        cursor = self.data.cursor()
        try:
            formeEpreuve = cursor.execute("SELECT distinct formeEp from lesEpreuves")

        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impo : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_formeEp, formeEpreuve)


    def refreshDisciplineEp(self):
        cursor = self.data.cursor()
        try:
            if self.ui.radioButton_insert.isChecked():
                nomDiscipline = cursor.execute("SELECT distinct nomDi from lesDisciplines")
            else:
                nomDiscipline= cursor.execute("SELECT distinct nomDi from lesEpreuves where numEp=?",[self.ui.comboBox_numEp.currentText()])

        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impos: " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_nomDi, nomDiscipline)

    def refreshCategorieEp(self):
        cursor = self.data.cursor()
        try:
            if self.ui.comboBox_formeEp.currentText() == "par couple":
                categorieEp= cursor.execute("SELECT distinct categorieEp from lesEpreuves where categorieEp='mixte'")
            else:
                categorieEp = cursor.execute("SELECT distinct categorieEp from lesEpreuves where categorieEp<>'mixte'")

        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer les categories: " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_categorieEp, categorieEp)




    def refreshNbSportifs(self):
        if self.ui.comboBox_formeEp.currentText() == "par couple":
            self.ui.spinBox_nbSportifs.setValue(2)
        elif self.ui.comboBox_formeEp.currentText() == "individuelle":
            self.ui.spinBox_nbSportifs.setValue(1)
        self.refreshNumInscrit()

    def refreshNumInscrit(self):
        cursor = self.data.cursor()
        try:
            if self.ui.comboBox_formeEp.currentText() == "par couple":
                res=cursor.execute("""
                WITH deuxMembres as(
                SELECT * from lesEquipes where nbEquipiersEq=2
                ),linkCategorie as(
                SELECT numSp,numEq,categorieSp from deuxMembres JOIN lesEquipiers using(numEq) JOIN lesSportifs_base using(numSp)
                )
                SELECT distinct l1.numEq from linkCategorie l1 JOIN linkCategorie l2 on(l1.numEq=l2.numEq AND l1.categorieSp<>l2.CategorieSp)""")
            elif self.ui.comboBox_formeEp.currentText() == "individuelle":
                res = cursor.execute("SELECT numSp from lesSportifs_base where categorieSp=?", [self.ui.comboBox_categorieEp.currentText()])
            else:
                res = cursor.execute("""
                WITH linkCategorie as(
                        SELECT E1.numSp,E1.numEq,categorieSp from lesEquipiers E1 JOIN lesEquipiers E2 using(numEq) JOIN lesSportifs_base using(numSp)
                )
                SELECT distinct l1.numEq 
                FROM linkCategorie l1 JOIN linkCategorie l2 
                ON (l1.numEq=l2.numEq and l1.numSp<>l2.numSp AND l1.categorieSp=? AND l2.categorieSp=?)
                """, [self.ui.comboBox_categorieEp.currentText(), self.ui.comboBox_categorieEp.currentText()])

        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer le numero d'inscrit : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_numIn, res)

    def refreshNumEpreuve(self):
        cursor = self.data.cursor()
        try:
            if self.ui.radioButton.isChecked():
                self.ui.lineEdit_nomEp.setEnabled(False)
                display.refreshLabel(self.ui.label_nomEp, "")
                self.ui.comboBox_numEp.setEnabled(True)
                display.refreshLabel(self.ui.label_numEp, "Numero de l'epreuve")
            else:
                display.refreshLabel(self.ui.label_nomEp, "Nom de l'epreuve")
                display.refreshLabel(self.ui.label_numEp, "")
                self.ui.comboBox_numEp.setEnabled(False)
                self.ui.lineEdit_nomEp.setEnabled(True)
            res = cursor.execute("SELECT distinct lesInscriptions.numEp from lesInscriptions JOIN lesEpreuves on(lesInscriptions.numEp =lesEpreuves.numEp AND categorieEp=? and formeEp=? ) WHERE lesInscriptions.numEp NOT IN (SELECT numEp from lesResultats) AND lesInscriptions.numEp NOT IN(SELECT numEp from lesInscriptions where numIn=?) ",[
               self.ui.comboBox_categorieEp.currentText(), self.ui.comboBox_formeEp.currentText(), self.ui.comboBox_numIn.currentText()
            ])
        except Exception as e:
            display.refreshLabel(self.ui.label_erreur, "Impossible de gerer le numero d'epreuve : " + repr(e))
        else:
            display.refreshGenericCombo(self.ui.comboBox_numEp, res)










