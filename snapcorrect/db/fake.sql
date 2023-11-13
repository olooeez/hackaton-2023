INSERT INTO professor (username, password) VALUES
    ('luiz', 'scrypt:32768:8:1$INyaXe99F7EAK1GA$f96f321f35d0d89b71e259c9e55db62ab69e6168a510201d723ec387e0a9d4f96aae5762c441a6ea334af94696cbaef293d90e8af2522dfd0de358cc55ce383b');

INSERT INTO test (professor_id, title) VALUES
    (1, 'Math 1'),
    (1, 'Math 2'),
    (1, 'Math 3'),
    (1, 'Physics 1'),
    (1, 'Chemistry 1'),
    (1, 'Biology 1');

INSERT INTO grade (title, professor_id) VALUES
    ('Class A', 1),
    ('Class B', 1),
    ('Class C', 1);

INSERT INTO student (username, professor_id, grade_id) VALUES
    ('Renan', 1, 1),
    ('Lucas', 1, 1),
    ('Raul', 1, 1),
    ('Maria', 1, 1),
    ('Pedro', 1, 1),
    ('Ana', 1, 1);
