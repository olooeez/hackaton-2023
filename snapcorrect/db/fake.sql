INSERT INTO professor (username, password) VALUES
    ('luiz', 'scrypt:32768:8:1$INyaXe99F7EAK1GA$f96f321f35d0d89b71e259c9e55db62ab69e6168a510201d723ec387e0a9d4f96aae5762c441a6ea334af94696cbaef293d90e8af2522dfd0de358cc55ce383b'),
    ('joao', 'scrypt:32768:8:1$INyaXe99F7EAK1GA$f96f321f35d0d89b71e259c9e55db62ab69e6168a510201d723ec387e0a9d4f96aae5762c441a6ea334af94696cbaef293d90e8af2522dfd0de358cc55ce383b'),
    ('alexandre', 'scrypt:32768:8:1$INyaXe99F7EAK1GA$f96f321f35d0d89b71e259c9e55db62ab69e6168a510201d723ec387e0a9d4f96aae5762c441a6ea334af94696cbaef293d90e8af2522dfd0de358cc55ce383b');

INSERT INTO test (professor_id, title) VALUES
    (1, 'Matemática 3'),
    (1, 'Matemática 2'),
    (1, 'Matemática 4');

INSERT INTO student (username, professor_id) VALUES
    ('Renan', 1),
    ('Lucas', 1),
    ('Raul', 1);
