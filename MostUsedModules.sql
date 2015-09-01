#by Edgars2007
USE urwiki_p;
SELECT Concat('[[ماڈیول:',tl_title,']]'), COUNT(tl_title)
FROM templatelinks
where tl_namespace=828# and tl_from_namespace=0
#and tl_title not like "VietasKarte/dati%"  and tl_title not like "%/doc"
group by tl_title
order by COUNT(tl_title) desc
limit 100
