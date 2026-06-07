import { Router } from 'express';
import { z } from 'zod';
import type { NotificationRepository } from '../domain/notification-repository.js';
import type { SendNotification } from '../domain/send-notification.js';

const createBody = z.object({
  userId: z.string().min(1),
  message: z.string().min(1),
  channel: z.enum(['email', 'sms', 'push']),
});

export function notificationRoutes(deps: {
  sendNotification: SendNotification;
  repository: NotificationRepository;
}): Router {
  const router = Router();

  router.post('/notifications', async (req, res) => {
    const parsed = createBody.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ errors: parsed.error.issues });
    }
    try {
      const result = await deps.sendNotification.execute(parsed.data);
      return res.status(201).json(result);
    } catch (err) {
      return res.status(400).json({ error: (err as Error).message });
    }
  });

  router.get('/notifications/:userId', async (req, res) => {
    const list = await deps.repository.findByUserId(req.params.userId);
    return res.json(list);
  });

  return router;
}
