import MySQLdb

def main():
   print(dbManagement.getInfoFromdb(dbManagement))

class dbManagement():
    def getInfoFromdb(self):

        jdbc = MySQLdb.connect(host='panel.vps100.nazwa.pl',
                               user='admin_zus',
                               passwd='zg7GRgo7oS',
                               db="admin_zus")

        cursor = jdbc.cursor()
        cursor.execute(" SELECT * FROM patients")
        results = cursor.fetchall()

        jdbc.close()
        return results


if __name__ == '__main__':
    main()
