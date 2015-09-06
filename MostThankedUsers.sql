SELECT log_title, COUNT(*) FROM logging
WHERE log_action = "thank"
GROUP BY log_title
ORDER BY COUNT(*) DESC
LIMIT 20;
