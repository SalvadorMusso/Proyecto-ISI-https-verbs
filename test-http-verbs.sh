#!/usr/bin/env bash
#
# demo-verbos-http.sh
#
# Demonstrates and verifies correct usage of the HTTP verbs
# (GET, POST, PATCH and DELETE) against a WSGI task server.
#
# Requirements:
#   - The server must be running on http://localhost:9292
#     (e.g.: uv run python server.py)
#   - curl installed
#
# Usage:
#   ./demo-verbos-http.sh
#
# Each check prints PASS or FAIL according to the status code and body
# returned by the server, and a machine-readable SUMMARY line is printed
# at the end. This script ALWAYS exits with 0 so it can be called from a
# grading script that parses the output (e.g., to grade many student
# repositories). To detect failures, look for "FAIL=0" in the SUMMARY
# line, or for the ERROR marker when the server is not reachable.
#
# You can override the base URL with the BASE environment variable:
#   BASE=http://localhost:9000 ./demo-verbos-http.sh

set -u

BASE="${BASE:-http://localhost:9292}"
BODY="$(mktemp)"
trap 'rm -f "$BODY"' EXIT

PASS=0
FAIL=0

if ! curl -s -o /dev/null "$BASE"; then
  echo "ERROR: cannot reach $BASE (is the server running?)"
  echo "SUMMARY: PASS=0 FAIL=1"
  exit 0
fi

# status <description> <expected codes> <curl args...>
# Runs curl, captures the status code and the body (into $BODY),
# and checks the status code against the space-separated expected codes.
status() {
  local desc="$1" expected="$2"
  shift 2
  local actual
  actual="$(curl -s -o "$BODY" -w "%{http_code}" "$@")"

  local ok=0 e
  for e in $expected; do
    [ "$actual" = "$e" ] && ok=1
  done

  if [ "$ok" = 1 ]; then
    echo "  PASS  $desc  ->  $actual"
    PASS=$((PASS + 1))
  else
    echo "  FAIL  $desc  ->  expected [$expected], got $actual"
    FAIL=$((FAIL + 1))
  fi
}

# body_has <description> <text to look for in the body>
body_has() {
  local desc="$1" pattern="$2"
  if grep -q -F "$pattern" "$BODY"; then
    echo "  PASS  $desc"
    PASS=$((PASS + 1))
  else
    echo "  FAIL  $desc  (not found: $pattern)"
    FAIL=$((FAIL + 1))
  fi
}

# Reads the "id" field from the last JSON response
extract_id() {
  python3 -c "import json,sys; print(json.load(sys.stdin)['id'])" < "$BODY"
}

echo
echo "== 1. GET /tasks (empty list at startup) =="
status "GET /tasks returns 200" "200" "$BASE/tasks"

echo
echo "== 2. POST /tasks creates a task and assigns an id =="
status "POST /tasks returns 201" "201" -X POST "$BASE/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Study HTTP", "done": false}'
body_has "the body returns the created task" "title"
body_has "the body includes an id" "id"
ID1="$(extract_id)"

echo
echo "== 3. A second POST creates another task with another id (POST is not idempotent) =="
status "POST /tasks returns 201" "201" -X POST "$BASE/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn PATCH", "done": false}'
ID2="$(extract_id)"
if [ -n "$ID1" ] && [ "$ID1" != "$ID2" ]; then
  echo "  PASS  each POST produces a different id  ($ID1 and $ID2)"
  PASS=$((PASS + 1))
else
  echo "  FAIL  two POSTs produced the same id ($ID1 / $ID2)"
  FAIL=$((FAIL + 1))
fi

echo
echo "== 4. GET /tasks returns the created tasks =="
status "GET /tasks returns 200" "200" "$BASE/tasks"

echo
echo "== 5. GET /tasks/$ID1 returns the created task =="
status "GET /tasks/$ID1 returns 200" "200" "$BASE/tasks/$ID1"
body_has "the body contains the original title" "Study HTTP"

echo
echo "== 6. PATCH /tasks/$ID1 updates only the sent field =="
status "PATCH /tasks/$ID1 returns 200" "200" -X PATCH "$BASE/tasks/$ID1" \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
body_has "done changed to true" '"done": true'
body_has "the title is preserved (PATCH is partial)" "Study HTTP"

echo
echo "== 7. DELETE /tasks/$ID1 deletes the task =="
status "DELETE /tasks/$ID1 returns 200 or 204" "200 204" -X DELETE "$BASE/tasks/$ID1"

echo
echo "== 8. GET /tasks/$ID1 returns 404 after deletion =="
status "GET /tasks/$ID1 returns 404" "404" "$BASE/tasks/$ID1"

echo
echo "== 9. GET /tasks/999 (nonexistent) returns 404 =="
status "GET /tasks/999 returns 404" "404" "$BASE/tasks/999"

echo
echo "== Summary =="
echo "SUMMARY: PASS=$PASS FAIL=$FAIL"
if [ "$FAIL" -gt 0 ]; then
  echo "Some checks failed. Review the status codes and the bodies."
else
  echo "All good! HTTP verbs are being used correctly."
fi

exit 0