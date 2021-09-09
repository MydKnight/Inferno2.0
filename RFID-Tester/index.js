const Sentry = require("@sentry/node");
const Tracing = require("@sentry/tracing");

Sentry.init({
  dsn: "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",

  // We recommend adjusting this value in production, or using tracesSampler for finer control
  tracesSampleRate: 1.0,
});

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('What do you think of Node.js? ', (answer) => {
  // TODO: Log the answer in a database
  console.log(`Thank you for your valuable feedback: ${answer}`);

  rl.close();
  
  throw new Error('listId does not exist');
});

