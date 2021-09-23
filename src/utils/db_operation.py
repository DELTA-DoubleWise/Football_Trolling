import pymysql

def sqldb(data_list):
    db = pymysql.connect(host="localhost", user="root", passwd="bujiangwude", database="hp", charset="utf8", port=3306)
    cursor = db.cursor()

    sql = 'INSERT INTO `hpNBA-all`(title,url,author,time,reply,view) VALUES(%s,%s,%s,%s,%s,%s)'
    try:
        cursor.executemany(sql, data_list)
        db.commit()
        print("execute successfully")
    except Exception as e:
        print("执行MySQL: %s 时出错：%s" % (sql, e))
        db.rollback()

    '''
    for data in data_list:
        title=data[0]
        url=data[1]
        author=data[2]
        time=data[3]
        reply=data[4]
        view=data[5]
        print(type(title))
        print(type(url))
        print(type(author))
        print(type(time))
        print(type(reply))
        print(type(view))
        try:
            sql = 'INSERT INTO `hpNBA-all`(title,url,author,time,reply,view)VALUES(%s,%s,%s,%s,%s,%d)'
            print(sql)
            cursor.execute(sql,(title,url,author,time,reply,view))
            db.commit()
        except Exception as e:
            print("执行MySQL: %s 时出错：%s" % (sql, e)) 
            db.rollback()
    '''
    db.close()