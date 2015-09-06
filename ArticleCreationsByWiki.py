# -*- coding: utf-8 -*-
import wikipedia, re
import pagegenerators
import MySQLdb as mysqldb
import config

def numbertopersian(a):
	a = str(a)
	a = a.replace(u'0', u'0')
	a = a.replace(u'1', u'1')
	a = a.replace(u'2', u'2')
	a = a.replace(u'3', u'3')
	a = a.replace(u'4', u'4')
	a = a.replace(u'5', u'5')
	a = a.replace(u'6', u'6')
	a = a.replace(u'7', u'7')
	a = a.replace(u'8', u'8')
	a = a.replace(u'9', u'9')
	a = a.replace(u'0', u'0')
	return a

savetext = u"{{#switch:{{{1|ur}}}"

# sql part
for lang in ["ur","fa","ar","ro","tr","en","fr","de","hi","az","id","pnb","hu","he"]:
	site = wikipedia.getSite(lang)
	query="select /* SLOW_OK */ count(rc_title),0 from recentchanges join page on rc_cur_id=page_id where rc_new=1 and rc_namespace=0 and page_is_redirect=0 and page.page_len>70 and rc_deleted=0 and DATE_SUB(CURRENT_TIMESTAMP, INTERVAL 1 DAY)<rc_timestamp;"

	conn = mysqldb.connect(lang+"wiki.labsdb", db = site.dbName(),
						   user = config.db_username,
						   passwd = config.db_password)
	cursor = conn.cursor()

	wikipedia.output(u'Executing query:\n%s' % query)
	query = query.encode(site.encoding())
	cursor.execute(query)

	wikinum,nunum = cursor.fetchone()
	if wikinum:
		savetext = savetext + u"|" + lang + u"=" + numbertopersian(wikinum)
		
# pywikipedia part
savetext = savetext + "}}"
wikipedia.output(savetext)
site = wikipedia.getSite()
page = wikipedia.Page(site,u"سانچہ:شماریات گذشتہ 24/شمار")
page.put(savetext,u"(روبالہ:تجديد شماريات")
