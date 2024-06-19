CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    employee_since DATE NOT NULL,
    age INTEGER NOT NULL
);

INSERT INTO staff (first_name, last_name, employee_since, age) VALUES
('Unni', 'Lozic', '2001-10-12', 47),
('Liv', 'Strömberg', '2012-03-27', 32),
('Ali', 'Sahib', '2015-12-15', 33);
