CREATE TABLE backlog(id VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, status VARCHAR NOT NULL, note VARCHAR, opened DATE NOT NULL, CHECK(regexp_matches(id, '^[a-z0-9]+(-[a-z0-9]+)*$')), CHECK((status IN ('open', 'in-progress', 'done'))));;
CREATE TABLE concepts(id VARCHAR PRIMARY KEY, "name" VARCHAR NOT NULL, "statement" VARCHAR NOT NULL, tags VARCHAR[] DEFAULT(main.list_value()) NOT NULL, CHECK(regexp_matches(id, '^[a-z0-9]+(-[a-z0-9]+)*$')));;
CREATE TABLE concept_sources(concept_id VARCHAR, source_id VARCHAR, PRIMARY KEY(concept_id, source_id));;
CREATE TABLE relations(from_id VARCHAR, to_id VARCHAR, relation VARCHAR, note VARCHAR, PRIMARY KEY(from_id, to_id, relation), CHECK((from_id != to_id)));;
CREATE TABLE session_log(id VARCHAR PRIMARY KEY, entry_date DATE NOT NULL, title VARCHAR NOT NULL, done VARCHAR NOT NULL, considered VARCHAR, rejected VARCHAR, CHECK(regexp_matches(id, '^[a-z0-9]+(-[a-z0-9]+)*$')));;
CREATE TABLE sources(id VARCHAR PRIMARY KEY, title VARCHAR NOT NULL, url VARCHAR NOT NULL, author VARCHAR, "year" INTEGER, CHECK(regexp_matches(id, '^[a-z0-9]+(-[a-z0-9]+)*$')), CHECK(starts_with(url, 'https://')));;

