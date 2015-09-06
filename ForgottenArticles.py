#!/usr/bin/env python
# encoding: utf-8
#Develop by Javad Yousefi // javad.y1@gmail.com
"""
ForgottenPages.py


Created by Tim Sears on 2012-03-16.
Copyright (c) Tim Sears. All rights reserved.
"""
##config
from config import *
import wikipedia
import MySQLdb
import config
import datetime

report_title=u'ویکیپیڈیا:رودادہائے ڈیٹابیس/فراموش شدہ مضامین'
report_template = u'''
{{ویکیپیڈیا:قاعدہ معطیات/سرنامہ}}
\n\n
<b>آخری تجدید:</b> ~~~~~\n
ذیل میں ان صفحات کی فہرست ہے جن میں گذشتہ دو سالوں سے کوئی ترمیم نہیں ہوئی۔

{| class="wikitable sortable"
|-
! مضمون
! آخری ترمیم
! عدد ترامیم
|-
%s
|}

[[زمرہ:ویکیپیڈیا رودادہائے قاعدہ معطیات]]
'''
##
query= '''SELECT /* SLOW_OK */ mp.page_title AS t, 
       TIMESTAMP((SELECT rev_timestamp 
                  FROM   revision 
                  WHERE  rev_id = mp.page_latest))                     AS ts, (SELECT COUNT(*) from revision where rev_page=mp.page_id) as ec,
(SELECT count(*) from templatelinks join page as tp on tp.page_title=tl_title and tp.page_namespace=10
join categorylinks as s on s.cl_to='Article_message_boxes' and s.cl_from=tp.page_id
where tl_namespace=10
and tl_from=mp.page_id) as tc
FROM   page as mp
LEFT OUTER JOIN  categorylinks as m
   ON  m.cl_to in ('Article_Feedback_Blacklist','All_set_index_articles','All_article_disambiguation_pages' )
   AND m.cl_from = mp.page_id
WHERE  mp.page_is_redirect = 0 
       AND mp.page_namespace = 0 
       AND mp.page_latest < (SELECT rev_id 
                          FROM   revision 
                          WHERE  rev_timestamp > Date_format(DATE_SUB(NOW(), 
                                                             INTERVAL 2 YEAR), 
                                                 '%Y%m%d%H%i%s') 
                          LIMIT  1) 
       AND m.cl_to IS NULL order by ts asc LIMIT 1000;'''
#db = connect(host=HOSTNAME, db=DATABSENAME, read_default_file='~/.my.cnf')
site  = wikipedia.getSite("ur")
db = MySQLdb.connect("urwiki.labsdb", db = site.dbName(),
                       user = config.db_username,
                       passwd = config.db_password)
					   
cursor=db.cursor()
#t=time()
print '* Running query "Forgotten Articles"...'
cursor.execute(query)
#print ':Done! Took %f seconds.'%(time()-t)
print '* Generating table...'
rows=''
for pagename,lastedit,editcount,maitnencecount in cursor.fetchall():
    rows+="""\n|[[:%s]]
    |%s
	|%s
    |-"""%(unicode(pagename.replace('_',' '),'utf-8'), lastedit,editcount)


print ':Done!'
rows=rows.replace(u'0',u'0').replace(u'1',u'1').replace(u'2',u'2').replace(u'3',u'3').replace(u'4',u'4').replace(u'5',u'5').replace(u'6',u'6').replace(u'7',u'7').replace(u'8',u'8').replace(u'9',u'9')
report_template=report_template%(rows)
report_page=wikipedia.Page(site,report_title)
report_page.put(report_template,comment=u'روبالہ:تجدید شماریات')
