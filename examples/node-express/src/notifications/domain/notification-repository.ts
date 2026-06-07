import type { NewNotification, Notification } from './notification.js';

export interface NotificationRepository {
  save(notification: NewNotification): Promise<Notification>;
  findByUserId(userId: string): Promise<Notification[]>;
}
