var serverStatus = require('express-server-status');
var express = require('express');
var url = require('url');
var _ = require('lodash');

var app = express();

app.set('port', (process.env.PORT || 5000));

app.use(express.static(__dirname + '/public'));

// views is directory for all template files
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.locals._ = _;

var middleware = {

    render: function (view) {
        return function (req, res, cb) {
            res.render(view);
        }
    },

    globalLocals: function (req, res, cb) {
        
        var url_parts = url.parse(req.url, true);
        var query = url_parts.query;
        var thing = serverStatus(app);
        res.locals = { 
            title: 'GOMOGO',
            sitebreakpoint: 'desktop',
            description: 'A site to help you move from location to location',
            query: query,
            param: {}
        };

        //overwrite locals based on query string
        if ( query.sitebreakpoint != undefined ) {
            res.locals.sitebreakpoint = query.sitebreakpoint
        }

        

        cb();
    },

    index: function (req, res, cb) {
        res.locals.index_specific_variable = 'somethingindexspecific';
        res.locals.template = 'home';
        cb();
    },

    article: function (req, res, cb) {
        res.locals.article_specific_variable = 'some article specifc variables';
        res.locals.template = 'article';
        cb();
    }

};

app.use('/status', serverStatus(app));

app.use(middleware.globalLocals);
app.get('/', middleware.index, middleware.render('template/index'));
app.get('/home', middleware.index, middleware.render('template/index'));
app.get('/questionnaire', middleware.index, middleware.render('template/questions'));
app.get('/result', middleware.index, middleware.render('template/result'));
app.get('/about', middleware.index, middleware.render('template/about'));

app.listen(app.get('port'), function() {
    console.log('Node app is running on port', app.get('port'));
});


