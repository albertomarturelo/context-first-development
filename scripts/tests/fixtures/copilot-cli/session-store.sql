-- Synthetic Copilot CLI session store: the column layout observed in 1.0.108,
-- invented rows. {PROJECT} and {OTHER} are replaced by the test harness.
-- input_tokens = uncached input + cache_read_tokens + cache_write_tokens.

CREATE TABLE sessions (id TEXT PRIMARY KEY, cwd TEXT, repository TEXT, host_type TEXT,
  branch TEXT, summary TEXT, created_at TEXT, updated_at TEXT);
CREATE TABLE turns (id INTEGER PRIMARY KEY, session_id TEXT, turn_index INTEGER,
  user_message TEXT, assistant_response TEXT, timestamp TEXT);
CREATE TABLE session_files (id INTEGER PRIMARY KEY, session_id TEXT, file_path TEXT,
  tool_name TEXT, turn_index INTEGER, first_seen_at TEXT);
CREATE TABLE assistant_usage_events (id INTEGER PRIMARY KEY, session_id TEXT, turn_index INTEGER,
  agent_id TEXT, parent_tool_call_id TEXT, model TEXT, copilot_usage_model TEXT,
  input_tokens INTEGER, output_tokens INTEGER, cache_read_tokens INTEGER,
  cache_write_tokens INTEGER, reasoning_tokens INTEGER, total_nano_aiu INTEGER,
  request_multiplier REAL, duration_ms INTEGER, time_to_first_token_ms INTEGER,
  output_ttft_ms REAL, inter_token_latency_ms INTEGER, initiator TEXT, api_endpoint TEXT,
  reasoning_effort TEXT, finish_reason TEXT, content_filter_triggered INTEGER,
  token_details_json TEXT, created_at TEXT, event_id TEXT);

INSERT INTO sessions VALUES
  ('cli-session-0001', '{PROJECT}', 'example/demo', 'github', 'feat/demo-56', 'SECRET-SUMMARY-TEXT',
   '2026-03-04T10:00:00.000Z', '2026-03-04T10:10:00.000Z'),
  ('cli-session-0002', '{OTHER}', 'example/other', 'github', 'main', 'SECRET-SUMMARY-TEXT',
   '2026-03-04T11:00:00.000Z', '2026-03-04T11:05:00.000Z');

INSERT INTO turns VALUES
  (1, 'cli-session-0001', 0, 'SECRET-PROMPT-TEXT', 'SECRET-RESPONSE-TEXT', '2026-03-04T10:00:00.000Z');

INSERT INTO session_files VALUES
  (1, 'cli-session-0001', '{PROJECT}/SECRET-FILE-PATH.py', 'apply_patch', 0, '2026-03-04T10:01:30.000Z');

INSERT INTO assistant_usage_events
  (id, session_id, turn_index, agent_id, parent_tool_call_id, model, input_tokens, output_tokens,
   cache_read_tokens, cache_write_tokens, reasoning_tokens, initiator, created_at)
VALUES
  -- turn 0: two main-agent requests, then one subagent request after the first edit
  (1, 'cli-session-0001', 0, NULL, NULL, 'model-c', 1500, 100, 1000, 300, 40, 'user', '2026-03-04T10:00:00.000Z'),
  (2, 'cli-session-0001', 0, NULL, NULL, 'model-c', 1800, 50, 1500, 200, 0, 'agent', '2026-03-04T10:01:00.000Z'),
  (3, 'cli-session-0001', 0, 'agent-x', 'call-1', 'model-c', 600, 30, 100, 0, 0, 'agent', '2026-03-04T10:02:00.000Z'),
  -- turn 1
  (4, 'cli-session-0001', 1, NULL, NULL, 'model-c', 2000, 80, 1900, 50, 0, 'user', '2026-03-04T10:10:00.000Z'),
  -- unreadable: no output count, then no usable timestamp
  (5, 'cli-session-0001', 1, NULL, NULL, 'model-c', 900, NULL, 800, 0, 0, 'agent', '2026-03-04T10:11:00.000Z'),
  (6, 'cli-session-0001', 1, NULL, NULL, 'model-c', 900, 10, 800, 0, 0, 'agent', 'not-a-date'),
  -- another project
  (7, 'cli-session-0002', 0, NULL, NULL, 'model-c', 700, 70, 600, 0, 0, 'user', '2026-03-04T11:00:00.000Z');
