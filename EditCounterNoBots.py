#!/usr/bin/python
# Abbas (Ar:User:Elph), 2012
# -*- coding: utf-8  -*-
import catlib ,pagegenerators
import wikipedia,urllib,gzip,codecs,re
import MySQLdb as mysqldb
import config
pagetop=u"'''تاریخ آخری تجدید:''''': ~~~~~ '''بذریعہ:''' [[user:{{subst:Currentuser}}|{{subst:Currentuser}}]]''\n\n"
pagetop+=u'\nفہرست 100 بلند پایہ صارفین بلحاظ شراکت بدون روبہ جات۔\n'
pagetop+=u'\nمزید دیکھیں: [[ویکیپیڈیا:رودادہائے ڈیٹابیس/فہرست ویکیپیڈیا صارفین بلحاظ شراکت|شماریات مع روبہ جات]]۔\n'
pagetop+=u'\n{| class="wikitable sortable"\n'
pagetop+=u'!شمار!!صارف!!شراکت\n|-\n'
pagedown=u'\n|}\n[[زمرہ:ویکیپیڈیا شماریات]]'
adress=u"ویکیپیڈیا:رودادہائے ڈیٹابیس/فہرست ویکیپیڈیا صارفین بلحاظ شراکت/بدون روبہ جات"
#adress=u"user:محمد شعیب/test44"
message=u"روبالہ:تجدید شماریات"
 
count=0
line_items=' '
rowfa=' '
rowic=' '
rowi=' '
rowit=' '
rowfi=' '
rowfia=' '
#---------------------------------------------- sql part--------------
site  = wikipedia.getSite("ur")
query = "SELECT user_name, user_editcount FROM user WHERE user_name NOT IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = 'bot') ORDER BY user_editcount DESC LIMIT 100;"
#query = "SELECT user_name, user_editcount FROM user WHERE user_name NOT 'روبہ خوش آمدید' AND user_name NOT IN (SELECT user_name FROM user_groups INNER JOIN user ON user_id = ug_user WHERE ug_group = 'bot') ORDER BY user_editcount DESC LIMIT 100;"
wikipedia.output(u'Executing query:\n%s' % query)
 
conn = mysqldb.connect("urwiki.labsdb", db = site.dbName(),
                       user = config.db_username,
                       passwd = config.db_password)
cursor = conn.cursor()
query = query.encode(site.encoding())
cursor.execute(query)
results = cursor.fetchall()
#---------------------------------------------- end of sql part---------
count=0
for row in results:
        count+=1
        rowi=unicode(str(row[0]),'UTF-8')
        rowi2=unicode(str(row[1]),'UTF-8')
        rowfa+=u'\n|'+str(count)+u'||[[user:'+rowi+u'|'+rowi+u']]||'
        rowfa+=u'[[special:Contributions/{{subst:formatnum:'+rowi+u'}}|{{subst:formatnum:'+rowi2+u'}}]]\n|-\n'
        text=rowfa.strip()
text=pagetop+text+pagedown
 
page = wikipedia.Page(site,adress)
page.put(text,message)
