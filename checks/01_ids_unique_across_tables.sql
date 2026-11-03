-- EXAMPLE: every table with an 'id' column shares one namespace, because render.py's cross-link
-- index is global (any id links to whatever row first defines it) - not just tables that feel
-- topically related. Add a table here whenever you add one with an 'id' column.
SELECT id, count(*) AS n FROM (
  SELECT id FROM concepts
  UNION ALL SELECT id FROM backlog
  UNION ALL SELECT id FROM session_log
) GROUP BY id HAVING count(*) > 1;
