from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_all_genes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM genes"""
            cursor.execute(query)

            for row in cursor:
                result.append(Gene(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_interactions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                           FROM interactions"""
            cursor.execute(query)

            for row in cursor:
                result.append(Interaction(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_classifications():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT * 
                        FROM classification"""
            cursor.execute(query)

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllLocalizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Localization 
from classification c 
order by Localization desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["Localization"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(loc):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct c.*, g.Essential, g.Chromosome
from classification c , genes g 
where c.GeneID = g.GeneID 
and c.Localization = %s"""
            cursor.execute(query,(loc,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllInteractions():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """select i.GeneID1, i.GeneID2 
                        from interactions i """
            cursor.execute(query)

            for row in cursor:
                result.append(row)

            cursor.close()
            cnx.close()
        return result
