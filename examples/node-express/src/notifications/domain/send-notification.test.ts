import { describe, expect, it } from 'vitest';
import { SendNotification } from './send-notification.js';
import type { NewNotification, Notification } from './notification.js';
import type { NotificationRepository } from './notification-repository.js';

class InMemoryNotificationRepository implements NotificationRepository {
  private store: Notification[] = [];

  async save(input: NewNotification): Promise<Notification> {
    const n: Notification = {
      id: `n-${this.store.length + 1}`,
      ...input,
      createdAt: new Date(),
    };
    this.store.push(n);
    return n;
  }

  async findByUserId(userId: string): Promise<Notification[]> {
    return this.store.filter((n) => n.userId === userId);
  }
}

describe('SendNotification', () => {
  it('rejects empty userId', async () => {
    const uc = new SendNotification(new InMemoryNotificationRepository());
    await expect(
      uc.execute({ userId: '', message: 'hi', channel: 'email' }),
    ).rejects.toThrow('userId is required');
  });

  it('rejects empty message', async () => {
    const uc = new SendNotification(new InMemoryNotificationRepository());
    await expect(
      uc.execute({ userId: 'u1', message: '   ', channel: 'sms' }),
    ).rejects.toThrow('message is required');
  });

  it('persists and returns a notification with id + createdAt', async () => {
    const repo = new InMemoryNotificationRepository();
    const uc = new SendNotification(repo);

    const result = await uc.execute({
      userId: 'u1',
      message: 'hello',
      channel: 'email',
    });

    expect(result.id).toBe('n-1');
    expect(result.createdAt).toBeInstanceOf(Date);
    expect(await repo.findByUserId('u1')).toHaveLength(1);
  });
});
