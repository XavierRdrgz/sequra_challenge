CREATE SCHEMA IF NOT EXISTS "raw_spacex";
CREATE TABLE IF NOT EXISTS "raw_spacex"."launchcrews" (
  "launch_id" text NOT NULL,
  "crew" text NOT NULL,
  "role" text NOT NULL,
  CONSTRAINT "launchcrews_pkey" PRIMARY KEY ("launch_id", "crew")
);
