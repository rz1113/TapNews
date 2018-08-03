var express = require('express');
var path = require('path');
var cors = require('cors');
var winston = require('winston');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

var bodyParser = require('body-parser');
//use body Parser middleware before any handler of POST request
app.use(bodyParser.json());

var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

var authCheckerMiddleware = require('./middleware/auth_checker');

var passport = require('passport');
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport'); 
var localLoginStrategy = require('./passport/login_passport'); 
passport.use('local-signup',localSignupStrategy);
passport.use('local-login',localLoginStrategy);

// TODO: remove this after development is done.
app.use(cors());

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static')));

app.use('/', index);
app.use('/auth', auth);
app.use('/news', authCheckerMiddleware);
app.use('/news', news);

// configure logging.
var logger = winston.createLogger({
  transports: [
    new(winston.transports.Console)({
      json: false,
      timestamp: true
    }),
    new winston.transports.File({
      filename: __dirname + '/debug.log',
      json: false
    })
  ],
  exceptionHandlers: [
    new(winston.transports.Console)({
      json: false,
      timestamp: true
    }),
    new winston.transports.File({
      filename: __dirname + '/exceptions.log',
      json: false
    })
  ],
  exitOnError: false
});

// catch 404 
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;
