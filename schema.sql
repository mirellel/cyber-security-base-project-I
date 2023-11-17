CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE titles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    content TEXT,
    posted_at TIMESTAMPTZ DEFAULT Now(),
    posted_by INTEGER REFERENCES users,
    topic_id INTEGER REFERENCES topics,
    visibility BOOLEAN
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    title_id INTEGER REFERENCES titles,
    commentor TEXT,
    sent_at TIMESTAMPTZ DEFAULT Now(),
    visibility BOOLEAN
);

CREATE TABLE likes(
    id SERIAL PRIMARY KEY,
    liker_id INTEGER REFERENCES users,
    title_id INTEGER REFERENCES titles
);