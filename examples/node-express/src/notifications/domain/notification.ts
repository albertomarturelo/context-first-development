export type Channel = 'email' | 'sms' | 'push';

export type Notification = {
  id: string;
  userId: string;
  message: string;
  channel: Channel;
  createdAt: Date;
};

export type NewNotification = Omit<Notification, 'id' | 'createdAt'>;
