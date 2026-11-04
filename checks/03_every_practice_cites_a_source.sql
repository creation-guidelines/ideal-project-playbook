-- Every practice cites at least one source (the template's rule: a factual claim needs a source).
-- A practice learned on a project cites where it was learned; one taken from a reference cites the reference.
SELECT c.id AS practice_without_a_source
FROM concepts c
WHERE c.id NOT IN (SELECT concept_id FROM concept_sources)
ORDER BY c.id;
