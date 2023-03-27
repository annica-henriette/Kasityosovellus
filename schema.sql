CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);

CREATE TABLE instructions (
    id SERIAL PRIMARY KEY, 
    creator_id INTEGER REFERENCES users, 
    name TEXT, 
    content TEXT, 
    difficulty INTEGER
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY, 
    creator_id INTEGER REFERENCES users, 
    name TEXT, 
    material TEXT, 
    start_date DATE, 
    finishing_date DATE, 
    instruction_used INTEGER REFERENCES instructions
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER REFERENCES users, 
    project_id INTEGER REFERENCES projects, 
    instruction_id INTEGER REFERENCES instructions, 
    stars INTEGER, 
    comment TEXT
);

