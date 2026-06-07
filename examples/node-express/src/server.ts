import { Pool } from 'pg';
import { buildApp } from './app.js';

const port = Number(process.env.PORT ?? 3000);
const pool = new Pool({ connectionString: process.env.DATABASE_URL });

const app = buildApp(pool);

app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`notifications service listening on http://localhost:${port}`);
});
