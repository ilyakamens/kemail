Kemail
======

A simple web app to send emails for free via other free email services such as SendGrid, Mailgun, and Mandrill.

Click <a href="https://ilyakamens.appspot.com">here</a> to try it.

## Technical Track

Back-end

## Technical choices

Python:
- No prior experience
- It seems to be a popular back-end language

Google App Engine
- No prior experience
- Seemed like a quick and easy way to get started

Back-end
- I'm not a huge fan of UI, so I chose a more back-end heavy project
- I've done back-end work in the past, but I've never written an API before or created a web service from scratch

## Trade-offs

- Focusing on the client's perspective took away from me designing more of an API
- Doing an entirely new project with no prior experience with any of the technologies was definitely a challenge

## With more time
- I would transform it more into an API. Right now the responses don't make use of HTTP status codes, and it's
  designed for someone using the web interface. In addition to making use of different HTTP status codes, I'd probably
  return a JSON encoded string with more detailed information.
- I don't have any automated tests as it wasn't built to be an API, so I'd test is as I transformed it. 
