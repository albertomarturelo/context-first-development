import express, { type Express } from 'express';
import type { Pool } from 'pg';
import { PostgresNotificationRepository } from './notifications/data/postgres-notification-repository.js';
import { SendNotification } from './notifications/domain/send-notification.js';
import { notificationRoutes } from './notifications/presentation/notification-routes.js';

export function buildApp(pool: Pool): Express {
  const app = express();
  app.use(express.json());

  const repository = new PostgresNotificationRepository(pool);
  const sendNotification = new SendNotification(repository);

  app.get('/health', (_req, res) => {
    res.json({ ok: true });
  });

  app.use(notificationRoutes({ sendNotification, repository }));

  return app;
}
