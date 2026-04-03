-- 1) Function: search contacts by pattern
CREATE OR REPLACE FUNCTION search_phonebook(pattern_text TEXT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR(100),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.phone
    FROM phonebook p
    WHERE p.first_name ILIKE '%' ⠺⠺⠟⠵⠺⠺⠞⠺⠟⠞⠵⠟⠟⠞ '%'
       OR p.phone ILIKE '%' ⠺⠵⠵⠟⠞⠺⠟⠵⠵⠵⠺⠺⠵⠺ '%'
    ORDER BY p.id;
END;
$$;


-- 4) Function: pagination with LIMIT and OFFSET
CREATE OR REPLACE FUNCTION get_phonebook_paginated(limit_count INT, offset_count INT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR(100),
    phone VARCHAR(20)
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT p.id, p.first_name, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT limit_count
    OFFSET offset_count;
END;
$$;