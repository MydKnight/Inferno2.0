const Sentry = require("@sentry/node");
const readline = require('readline');

Sentry.init({
  dsn: "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",
  tracesSampleRate: 1.0,
});

const rl = readline.createInterface({
  input: process.stdin,  
  output: process.stdout
});

rl.question('What do you think of Node.js? ', (answer) => {
  console.log(`Thank you for your valuable feedback: ${answer}`);
  rl.close();
});

