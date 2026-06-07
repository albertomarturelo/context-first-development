import type { Pool } from 'pg';
import type { NotificationRepository } from '../domain/notification-repository.js';
import type {
  Channel,
  NewNotification,
  Notification,
} from '../domain/notification.js';

type DbRow = {
  id: string;
  user_id: string;
  message: string;
  channel: Channel;
  created_at: Date;
};

function toDomain(r: DbRow): Notification {
  return {
    id: r.id,
    userId: r.user_id,
    message: r.message,
    channel: r.channel,
    createdAt: r.created_at,
  };
}

export class PostgresNotificationRepository implements NotificationRepository {
  constructor(private readonly pool: Pool) {}

  async save(input: NewNotification): Promise<Notification> {
    const result = await this.pool.query<DbRow>(
      `INSERT INTO notifications (user_id, message, channel)
       VALUES ($1, $2, $3)
       RETURNING id, user_id, message, channel, created_at`,
      [input.userId, input.message, input.channel],
    );
    return toDomain(result.rows[0]);
  }

  async findByUserId(userId: string): Promise<Notification[]> {
    const result = await this.pool.query<DbRow>(
      `SELECT id, user_id, message, channel, created_at
         FROM notifications
        WHERE user_id = $1
        ORDER BY created_at DESC`,
      [userId],
    );
    return result.rows.map(toDomain);
  }
}
