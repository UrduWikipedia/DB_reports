#!/usr/bin/python
# Abbas (Ar:User:Elph), 2012
# -*- coding: utf-8  -*-
import catlib ,pagegenerators
import wikipedia,urllib,gzip,codecs,re
import MySQLdb as mysqldb
import config
pagetop=u"'''تاریخ آخری تجدید:''''': ~~~~~ '''بذریعہ:''' [[user:{{subst:Currentuser}}|{{subst:Currentuser}}]]''\n\n"
pagetop+=u'\nیہ 500 ویکیپیڈیا صارفین کی فہرست ہے جن میں [[ویکیپیڈیا:روبہ جات|روبہ جات]] بھی شامل ہیں۔\n'
pagetop+=u'\nمزید دیکھیں: [[ویکیپیڈیا:رودادہائے ڈیٹابیس/فہرست ویکیپیڈیا صارفین بلحاظ شراکت/بدون روبہ جات|فہرست صارفین بدون روبہ جات]]\n'
pagetop+=u'\n{| class="wikitable sortable"\n'
pagetop+=u'!شمار!!صارف!!تعداد ترامیم!!اندراج!!اولین ترمیم!!اختیارات\n|-\n'
pagedown=u'\n|}\n[[زمرہ:ویکیپیڈیا شماریات]]'
adress=u"ویکیپیڈیا:رودادہائے ڈیٹابیس/فہرست ویکیپیڈیا صارفین بلحاظ شراکت"
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
query =('''
  SELECT DISTINCT
  user_name,
  user_editcount,
  user_registration,
  rev_timestamp,
  GROUP_CONCAT(ug_group)
FROM user
JOIN user_groups
ON ug_user = user_id
JOIN revision
ON rev_user = user_id
AND (SELECT
       MIN(rev_timestamp)
     FROM revision
     WHERE rev_user = user_id)
AND rev_timestamp = (SELECT
                       MIN(rev_timestamp)
                     FROM revision
                     WHERE rev_user = user_id)
GROUP BY user_editcount DESC LIMIT 100;
''')
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
        rowi3=unicode(str(row[2]),'UTF-8')
        rowi4=unicode(str(row[3]),'UTF-8')
        rowi5=unicode(str(row[4]),'UTF-8')
        #rowi3=str(mytime)
        Year=rowi3 [0:4]
        Month=rowi3[4:6]
        Day=rowi3[6:8]
        hor=rowi3[8:10]
        Min=rowi3[10:12]
        sec=rowi3[12:14]
        Month=Month.replace(u'01',u'جنوری').replace(u'02',u'فروری').replace(u'03',u'اپریل').replace(u'04',u'مئی').replace(u'05',u'مارچ').replace(u'06',u'جون').replace(u'07',u'جولائی').replace(u'08',u'اگست').replace(u'09',u'ستمبر').replace(u'10',u'اکتوبر').replace(u'11',u'نومبر').replace(u'12',u'دسمبر')
        Year2=rowi4 [0:4]
        Month2=rowi4[4:6]
        Day2=rowi4[6:8]
        hor2=rowi4[8:10]
        Min2=rowi4[10:12]
        sec2=rowi4[12:14]
        Month2=Month2.replace(u'01',u'جنوری').replace(u'02',u'فروری').replace(u'03',u'اپریل').replace(u'04',u'مئی').replace(u'05',u'مارچ').replace(u'06',u'جون').replace(u'07',u'جولائی').replace(u'08',u'اگست').replace(u'09',u'ستمبر').replace(u'10',u'اکتوبر').replace(u'11',u'نومبر').replace(u'12',u'دسمبر')
        #rowi4=unicode(str(row[3]),'UTF-8')
        rowfa+=u'\n|bgcolor="#808080"|'+str(count)+u'||bgcolor="#D3D3D3"|[[user:'+rowi+u'|'+rowi+u']]||'
        rowfa+=u'bgcolor="#DCDCDC"|[[خاص:شراکتیں/{{subst:formatnum:'+rowi+u'}}|{{subst:formatnum:'+rowi2+u'}}]]||'
        #rowfa+=rowi3+'\n|-\n'
        rowfa+=u'bgcolor="#E5E4E2"|'+Day+u' '+Month+u' '+Year+u' <small>بوقت ('+hor+u':'+Min+u':'+sec+u')</small>||'
        rowfa+=u'bgcolor="#E5E4E2"|'+Day2+u' '+Month2+u' '+Year2+u' <small>بوقت ('+hor2+u':'+Min2+u':'+sec2+u')</small>||'
        rowfa=rowfa.replace(u'None',u'نامعلوم')
        rowfa=rowfa.replace(u'نامعلوم <small>بوقت (::)</small>',u'نامعلوم')
        #rowfa+=rowi4+u'||\n'
        rowi5=rowi5.replace(u'bot',u'[[ویکیپیڈیا:روبہ جات|روبہ]]').replace(u'rollbacker',u'[[ویکیپیڈیا:استرجع|استرجع کنندہ]]').replace(u'confirmed',u'[[ویکیپیڈیا:توثیق شدہ صارفین|توثیق شدہ صارف]]').replace(u'ipblock-exempt',u'[[ویکیپیڈیا:استثناءات از دستور شبکی (IP) پابندی|مستثنی از دستور شبکی]]').replace(u'import',u'[[ویکیپیڈیا:درآمدکنندگان|درآمدکنندہ]]').replace(u'sysop',u'[[ویکیپیڈیا:منتظمین|منتظم]]').replace(u'bureaucrat',u'[[ویکیپیڈیا:مامورین اداری|مامور اداری]]').replace(u'abusefilter',u'[[ویکیپیڈیا:مقطار غلط کاری|منتظم مقطار غلط کاری]]')
        rowfa+=rowi5+'\n|-\n'
        text=rowfa.strip()
text=pagetop+text+pagedown
page = wikipedia.Page(site,adress)
page.put(text,message)
