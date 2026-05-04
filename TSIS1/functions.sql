-- Functions for search and pagination.

-- Extended search: name, main phone, email, group, and all phones.
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    birthday DATE,
    group_name VARCHAR(50)
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        p.id,
        p.first_name,
        p.phone,
        p.email,
        p.birthday,
        g.name AS group_name
    FROM phonebook p
    LEFT JOIN groups g ON p.group_id = g.id
    LEFT JOIN phones ph ON ph.contact_id = p.id
    WHERE p.first_name ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
       OR p.email ILIKE '%' || p_query || '%'
       OR g.name ILIKE '%' || p_query || '%'
       OR ph.phone ILIKE '%' || p_query || '%'
    ORDER BY p.id;
END;
$$;


-- Compatibility function from Practice 8.
CREATE OR REPLACE FUNCTION search_phonebook(pattern_text TEXT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    birthday DATE,
    group_name VARCHAR(50)
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT *
    FROM search_contacts(pattern_text);
END;
$$;


-- Pagination with LIMIT and OFFSET.
CREATE OR REPLACE FUNCTION get_phonebook_paginated(limit_count INT, offset_count INT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    birthday DATE,
    group_name VARCHAR(50)
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT
        p.id,
        p.first_name,
        p.phone,
        p.email,
        p.birthday,
        g.name AS group_name
    FROM phonebook p
    LEFT JOIN groups g ON p.group_id = g.id
    ORDER BY p.id
    LIMIT limit_count
    OFFSET offset_count;
END;
$$;