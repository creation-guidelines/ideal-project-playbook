COPY backlog FROM 'data/backlog.json' (FORMAT 'json');
COPY concepts FROM 'data/concepts.json' (FORMAT 'json');
COPY concept_sources FROM 'data/concept_sources.json' (FORMAT 'json');
COPY relations FROM 'data/relations.json' (FORMAT 'json');
COPY session_log FROM 'data/session_log.json' (FORMAT 'json');
COPY sources FROM 'data/sources.json' (FORMAT 'json');
