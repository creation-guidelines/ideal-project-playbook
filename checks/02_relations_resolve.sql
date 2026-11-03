-- Both ends of every relation must be an existing id, in any table that has one (see 01's note).
WITH ids AS (
  SELECT id FROM concepts UNION ALL SELECT id FROM backlog UNION ALL SELECT id FROM session_log
)
SELECT 'from_id' AS end_, from_id AS missing_id FROM relations WHERE from_id NOT IN (SELECT id FROM ids)
UNION ALL
SELECT 'to_id', to_id FROM relations WHERE to_id NOT IN (SELECT id FROM ids);
