-- Stored procedures for the improved phonebook project.

-- Practice 8 compatibility: insert or update by phone.
CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS
$$
DECLARE
    v_contact_id INT;
BEGIN
    INSERT INTO phonebook (first_name, phone)
    VALUES (p_name, p_phone)
    ON CONFLICT (phone)
    DO UPDATE SET first_name = EXCLUDED.first_name
    RETURNING id INTO v_contact_id;

    IF v_contact_id IS NULL THEN
        SELECT id INTO v_contact_id
        FROM phonebook
        WHERE phone = p_phone;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, 'mobile')
    ON CONFLICT (contact_id, phone) DO NOTHING;
END;
$$;


-- Practice 8 compatibility: bulk insert with simple validation.
CREATE OR REPLACE PROCEDURE insert_many_users(
    p_names VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql
AS
$$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_names[i] IS NULL OR trim(p_names[i]) = '' THEN
            RAISE NOTICE 'Skipped row %: empty name', i;
        ELSIF p_phones[i] IS NULL OR trim(p_phones[i]) = '' THEN
            RAISE NOTICE 'Skipped row %: empty phone', i;
        ELSE
            CALL insert_or_update_user(p_names[i], p_phones[i]);
        END IF;
    END LOOP;
END;
$$;


-- Practice 8 compatibility: delete by username or phone.
CREATE OR REPLACE PROCEDURE delete_user(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS
$$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value
       OR phone = p_value
       OR id IN (
            SELECT contact_id
            FROM phones
            WHERE phone = p_value
       );
END;
$$;


-- New procedure: add a new phone number to an existing contact.
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS
$$
DECLARE
    v_contact_id INT;
BEGIN
    SELECT id INTO v_contact_id
    FROM phonebook
    WHERE first_name = p_contact_name
    ORDER BY id
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Phone type must be home, work, or mobile';
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO NOTHING;
END;
$$;


-- New procedure: move contact to a group. Creates the group if it does not exist.
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS
$$
DECLARE
    v_group_id INT;
BEGIN
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE phonebook
    SET group_id = v_group_id
    WHERE first_name = p_contact_name;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
END;
$$;