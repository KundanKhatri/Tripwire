-- TripWire attack corpus schema. Apply once after provisioning Cosmos for Postgres.
-- Requires the `vector` extension (enable in Cosmos cluster settings).

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS attack_patterns (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  attack_type text NOT NULL,
  owasp_category text NOT NULL,
  payload text NOT NULL,
  source_ref text,
  embedding vector(3072),
  severity int NOT NULL DEFAULT 5,
  added_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_attack_patterns_embedding
  ON attack_patterns USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_attack_patterns_owasp
  ON attack_patterns (owasp_category);

CREATE TABLE IF NOT EXISTS defense_traces (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id uuid NOT NULL,
  arena_session_id uuid,
  payload text NOT NULL,
  verdict text NOT NULL CHECK (verdict IN ('allow', 'review', 'block')),
  layers jsonb NOT NULL,
  explanation text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_defense_traces_created
  ON defense_traces (created_at DESC);

CREATE TABLE IF NOT EXISTS canaries (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  token text UNIQUE NOT NULL,
  request_id uuid NOT NULL,
  expires_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_canaries_token ON canaries (token);
CREATE INDEX IF NOT EXISTS idx_canaries_expires ON canaries (expires_at);

CREATE TABLE IF NOT EXISTS arena_attempts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  attacker_handle text,
  payload text NOT NULL,
  verdict text NOT NULL,
  score int NOT NULL DEFAULT 0,
  trace_id uuid REFERENCES defense_traces(id),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_arena_score
  ON arena_attempts (score DESC, created_at DESC);
