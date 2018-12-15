const functions = require('firebase-functions');
const request = require('request-promise');

const LINE_MESSAGING_API = 'https://api.line.me/v2/bot/message';
const LINE_HEADER = {
  'Content-Type': 'application/json',
  Authorization: `Bearer ju6SSFd7MGasmLZH5zJGSRGZGxojb0K5YZJXZa2OzvPaFIgpyTnEd31a4VEp85TY8vDnoTr9bnQyf5ZvHW/tEFWRKbOiuQUuErl207+KEXlUuJtM0JOr6sZXKLmOI8m9SbA1i12SvwFOX35aXFNvcAdB04t89/1O/w1cDnyilFU=`
};

exports.LineBot = functions.https.onRequest((req, res) => {
  if (!req.body || !req.body.events) {
    return res.send('Hello world!');
  }
  if (req.body.events[0].message.type !== 'text') {
    return null;
  }
  return reply(req.body);
});

const reply = bodyResponse => {
  return request({
    method: `POST`,
    uri: `${LINE_MESSAGING_API}/reply`,
    headers: LINE_HEADER,
    body: JSON.stringify({
      replyToken: bodyResponse.events[0].replyToken,
      messages: [
        {
          type: `text`,
          text: bodyResponse.events[0].message.text
        }
      ]
    })
  });
};
