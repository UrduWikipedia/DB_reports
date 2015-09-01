#by Edgars2007
SELECT CONCAT('[[ماڈیول:',tl_title,']]'), COUNT(tl_title)
FROM templatelinks
WHERE tl_namespace=828
GROUP BY tl_title
ORDER BY COUNT(tl_title) DESC
LIMT 100
