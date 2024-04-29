CREATE SCHEMA IF NOT EXISTS "raw_spacex";
CREATE TABLE IF NOT EXISTS "raw_spacex"."launchcores" (
  "launch_id" text NOT NULL,
  "core" text NOT NULL,
  "flight" integer,
  "gridfins" boolean,
  "legs" boolean,
  "reused" boolean,
  "landing_attempt" boolean,
  "landing_success" boolean,
  "landing_type" text,
  "landpad" text,
  CONSTRAINT "launchcores_pkey" PRIMARY KEY ("launch_id", "core")
);