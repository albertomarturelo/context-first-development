import type { NotificationRepository } from './notification-repository.js';
import type { NewNotification, Notification } from './notification.js';

export class SendNotification {
  constructor(private readonly repo: NotificationRepository) {}

  async execute(input: NewNotification): Promise<Notification> {
    if (!input.userId.trim()) {
      throw new Error('userId is required');
    }
    if (!input.message.trim()) {
      throw new Error('message is required');
    }
    return this.repo.save(input);
  }
}
