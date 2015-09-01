SELECT CONCAT('[[',p.page_title,']]') as نام_مضمون,
CONCAT('[[User:',r.rev_user_text,'|',r.rev_user_text,']]') as صارف_نام,
p.page_len as Size from revision r, page p 
WHERE r.rev_parent_id = 0 
AND r.rev_len < 2048 
AND p.page_len < 2048 
AND p.page_namespace = 0 
AND p.page_is_redirect = 0 
AND rev_timestamp < '2015900000000' 
AND rev_timestamp > '20150731235959' 
AND r.rev_page = p.page_id;
