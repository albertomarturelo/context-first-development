import { Pool } from 'pg';
import { afterAll, beforeAll, beforeEach, describe, expect, it } from 'vitest';
import { PostgresNotificationRepository } from './postgres-notification-repository.js';

// Integration test — talks to the real Postgres in docker-compose.test.yml.
// See ADR-003 for why mocks are not allowed in this layer.
const pool = new Pool({
  connectionString:
    process.env.TEST_DATABASE_URL ??
    'postgres://cfd:cfd@localhost:5433/cfd_test',
});

describe('PostgresNotificationRepository', () => {
  beforeAll(async () => {
    await pool.query(`
      CREATE EXTENSION IF NOT EXISTS "pgcrypto";
      CREATE TABLE IF NOT EXISTS notifications (
        id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id     TEXT        NOT NULL,
        message     TEXT        NOT NULL,
        channel     TEXT        NOT NULL CHECK (channel IN ('email','sms','push')),
        created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
      );
    `);
  });

  beforeEach(async () => {
    await pool.query('TRUNCATE notifications');
  });

  afterAll(async () => {
    await pool.end();
  });

  it('saves and reads back a notification', async () => {
    const repo = new PostgresNotificationRepository(pool);

    await repo.save({ userId: 'u1', message: 'hello', channel: 'email' });

    const list = await repo.findByUserId('u1');
    expect(list).toHaveLength(1);
    expect(list[0].userId).toBe('u1');
    expect(list[0].message).toBe('hello');
    expect(list[0].channel).toBe('email');
    expect(list[0].id).toMatch(/^[0-9a-f-]{36}$/i);
  });

  it('orders results by createdAt desc', async () => {
    const repo = new PostgresNotificationRepository(pool);

    await repo.save({ userId: 'u1', message: 'first', channel: 'email' });
    await new Promise((r) => setTimeout(r, 10));
    await repo.save({ userId: 'u1', message: 'second', channel: 'sms' });

    const list = await repo.findByUserId('u1');
    expect(list.map((n) => n.message)).toEqual(['second', 'first']);
  });

  it('isolates notifications by userId', async () => {
    const repo = new PostgresNotificationRepository(pool);

    await repo.save({ userId: 'u1', message: 'for u1', channel: 'email' });
    await repo.save({ userId: 'u2', message: 'for u2', channel: 'push' });

    const listU1 = await repo.findByUserId('u1');
    expect(listU1).toHaveLength(1);
    expect(listU1[0].userId).toBe('u1');
  });
});
