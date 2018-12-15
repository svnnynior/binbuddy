const functions = require('firebase-functions');
const request = require('request-promise');

const LINE_MESSAGING_API = 'https://api.line.me/v2/bot/message';
const LINE_HEADER = {
  'Content-Type': 'application/json',
  Authorization: `Bearer xxxx`
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
