CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name character varying(40),
    age integer,
    password character varying
);

CREATE FUNCTION sum_of_ages()
RETURNS integer AS $$
    DECLARE
        sum integer;
        rec record;
    BEGIN
        sum = 0;
        FOR rec IN SELECT * FROM users LOOP
            sum = sum + rec.age;
        END LOOP;
        RETURN sum;
    END;
$$ LANGUAGE plpgsql;
