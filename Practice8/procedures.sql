-- 2) Procedure: insert or update one user
CREATE OR REPLACE PROCEDURE insert_or_update_user(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql
AS
$$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE first_name = p_name
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- helper table for incorrect data
CREATE TABLE IF NOT EXISTS incorrect_data (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    phone VARCHAR(20),
    reason TEXT
);


-- 3) Procedure: insert many users with validation
CREATE OR REPLACE PROCEDURE insert_many_users(
    IN names_arr TEXT[],
    IN phones_arr TEXT[]
)
LANGUAGE plpgsql
AS
$$
DECLARE
    i INT;
    current_name TEXT;
    current_phone TEXT;
BEGIN
    IF array_length(names_arr, 1) IS DISTINCT FROM array_length(phones_arr, 1) THEN
        RAISE EXCEPTION 'Names array and phones array must have the same length';
    END IF;

    FOR i IN 1..array_length(names_arr, 1)
    LOOP
        current_name := names_arr[i];
        current_phone := phones_arr[i];

        -- simple validation: phone must contain only digits and length = 11
        IF current_phone !~ '^[0-9]{11}$' THEN
            INSERT INTO incorrect_data(first_name, phone, reason)
            VALUES (current_name, current_phone, 'Invalid phone format');
        ELSE
            IF EXISTS (
                SELECT 1
                FROM phonebook
                WHERE first_name = current_name
            ) THEN
                UPDATE phonebook
                SET phone = current_phone
                WHERE first_name = current_name;
            ELSE
                INSERT INTO phonebook(first_name, phone)
                VALUES (current_name, current_phone);
            END IF;
        END IF;
    END LOOP;
END;
$$;


-- function to return all incorrect data
CREATE OR REPLACE FUNCTION get_incorrect_data()
RETURNS TABLE(
    id INT,
    first_name VARCHAR(100),
    phone VARCHAR(20),
    reason TEXT
)
LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN QUERY
    SELECT d.id, d.first_name, d.phone, d.reason
    FROM incorrect_data d
    ORDER BY d.id;
END;
$$;


-- 5) Procedure: delete by name or phone
CREATE OR REPLACE PROCEDURE delete_user(p_value TEXT)
LANGUAGE plpgsql
AS
$$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value
       OR phone = p_value;
END;
$$;