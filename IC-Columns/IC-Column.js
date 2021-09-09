const Sentry = require("@sentry/node");
const readline = require("readline");
const GPIO = require("onoff").Gpio;

Sentry.init({
  dsn: "https://53058513222b41498b342be101261452@o358570.ingest.sentry.io/3153173",
  tracesSampleRate: 1.0,
});

const redLED = new Gpio(16, "out");
const redButton = new Gpio(13, "in", "both");

redButton.watch(function (err, value) {
  if (err) {
    console.error("There was an error", err);
    return;
  }
  redLED.writeSync(value);
});

function unexportOnClose() {
  redLED.writeSync(0);
  redLED.unexport();
  redButton.unexport();
}

// CLean Up on Ctrl+C
process.on("SIGINT", unexportOnClose);
