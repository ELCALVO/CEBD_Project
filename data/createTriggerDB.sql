CREATE trigger IF NOT EXISTS only100equipes
    BEFORE INSERT on lesEquipiers
        BEGIN
            SELECT CASE
                WHEN ((SELECT count(distinct numEq) from lesEquipiers)>100)
                    THEN RAISE(ABORT,'Pas plus de 100 équipes')
                END;
            END
/

CREATE trigger IF NOT EXISTS only500sportifs
    BEFORE INSERT on lesSportifs_base
        BEGIN
            SELECT CASE
                WHEN ((SELECT count(distinct numSp) from lesSportifs_base)>500)
                    THEN RAISE(ABORT,'Pas plus de 500 sportifs')
                END;
            END
/



