import psycopg2
def connect(dbname="news"):
    try:
        marwan = psycopg2.connect("dbname={}".format(dbname))
        c = marwan.cursor()
        return marwan, c
    except:
        print("Error in connecting to database")

def view_popular_article():
    try:
        marwan, c = connect()
        query = "create or replace view popular_articles as\
        select title,count(title) as views from articles,log\
        where log.path = concat('/article/',articles.slug)\
        group by title order by views desc"
        c.execute(query)
        marwan.commit()
        marwan.close()
    except:
        print("Error in creating view popular_articles")

def view_popular_authors():
    try:
        marwan, c = connect()
        query= "create or replace view popular_authors as select authors.name,\
        count(articles.author) as views from articles, log, authors where\
        log.path = concat('/article/',articles.slug) and\
        articles.author = authors.id group by authors.name order by views desc"
        c.execute(query)
        marwan.commit()
        marwan.close()
    except:
        print("Error in creating view popular_authors")

def view_log_status():
    try:
        marwan, c = connect()
        query = "create or replace view log_status as select Date,Total,Error,\
        (Error::float*100)/Total::float as Percent from\
        (select time::timestamp::date as Date, count(status) as Total,\
        sum(case when status = '404 NOT FOUND' then 1 else 0 end) as Error\
        from log group by time::timestamp::date) as result\
        where (Error::float*100)/Total::float > 1.0 order by Percent desc;"
        c.execute(query)
        marwan.commit()
        marwan.close()
    except:
        print("Error in creating view log_status")

def popular_article():
    marwan, c = connect()
    query = "select * from popular_articles limit 3"
    c.execute(query)
    result = c.fetchall()
    marwan.close()
    print "\nPopular Articles:\n"
    for i in range(0, len(result), 1):
        print "\"" + result[i][0] + "\" - " + str(result[i][1]) + " views"

def popular_authors():
    marwan, c = connect()
    query = "select * from popular_authors"
    c.execute(query)
    result = c.fetchall()
    marwan.close()
    print "\nPopular Authors:\n"
    for i in range(0, len(result), 1):
        print "\"" + result[i][0] + "\" - " + str(result[i][1]) + " views"

def log_status():
    marwan, c = connect()
    query = "select * from log_status"
    c.execute(query)
    result = c.fetchall()
    marwan.close()
    print "\nDays with more than 1% of errors:\n"
    for i in range(0, len(result), 1):
        print str(result[i][0])+ " - "+str(round(result[i][3], 2))+"% errors"

if __name__ == '__main__':
    view_popular_article()
    view_popular_authors()
    view_log_status()
    popular_article()
    popular_authors()
    log_status()
    print "\nSuccess!\n"
