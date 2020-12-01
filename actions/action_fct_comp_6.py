import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction 6
class AppFctComp6(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_6.ui", self)
        self.data = data
        self.refreshResult()

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_6, "")
        try:
            cursor = self.data.cursor()
            requete = """WITH lesPays as(
    SELECT distinct pays
    from LesSportifs_base
),
Equipes_pays_gold as (
    SELECT pays, count(distinct gold) AS nbGold
    FROM LesSportifs S JOIN LesEquipiers L on (S.numSp = L.numSp) JOIN lesResultats R on (R.gold=L.numEq)
    GROUP BY pays
),
Equipes_pays_silver as (
    SELECT pays, count(distinct silver) AS nbSilver
    FROM LesSportifs S JOIN LesEquipiers L on (S.numSp = L.numSp) JOIN lesResultats R on (R.silver=L.numEq)
    GROUP BY pays
),
Equipes_pays_bronze as (
    SELECT pays, count(distinct bronze) AS nbBronze
    FROM LesSportifs S JOIN LesEquipiers L on (S.numSp = L.numSp) JOIN lesResultats R on (R.bronze=L.numEq)
    GROUP BY pays
),
Solo_pays_gold as (
    SELECT pays,count(distinct gold) AS nbGold
    FROM LesSportifs S JOIN LesResultats R on S.numSp = R.gold
    GROUP by pays
),
Solo_pays_silver as (
    SELECT pays,numSp,count(distinct silver) AS nbSilver
    FROM LesSportifs S JOIN LesResultats R on S.numSp = R.silver
    GROUP by pays
),
Solo_pays_bronze as (
    SELECT pays,numSp,count(distinct bronze) AS nbBronze
    FROM LesSportifs S JOIN LesResultats R on S.numSp = R.bronze
    GROUP by pays
),
TotalGold as (
    SELECT p.pays,ifnull(S.nbGold,0)+ifnull(E.nbGold,0) as nbGold
    FROM   lesPays P LEFT OUTER JOIN Solo_pays_gold S ON (P.pays=S.pays) LEFT OUTER JOIN Equipes_pays_gold E ON(E.pays=P.pays)
),
TotalSilver as(
    SELECT p.pays,ifnull(S.nbSilver,0)+ifnull(E.nbSilver,0) as nbSilver
    FROM   lesPays P LEFT OUTER JOIN Solo_pays_silver S ON (P.pays=S.pays) LEFT OUTER JOIN Equipes_pays_silver E ON(E.pays=P.pays)
),
TotalBronze as(
    SELECT p.pays,ifnull(S.nbBronze,0)+ifnull(E.nbBronze,0) as nbBronze
    FROM   lesPays P LEFT OUTER JOIN Solo_pays_bronze S ON (P.pays=S.pays) LEFT OUTER JOIN Equipes_pays_bronze E ON(E.pays=P.pays)
)

SELECT TotalGold.pays,nbGold, nbSilver, nbBronze from  TotalGold JOIN TotalSilver using(pays) JOIN TotalBronze using(pays) 
ORDER BY nbGold DESC, nbSilver DESC, nbBronze DESC;"""
            result = cursor.execute(requete)
        except Exception as e:
            self.ui.table_fct_comp_6.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_6, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_6, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_6, "Aucun résultat")