var es = require('elasticsearch');
var through = require('through')
var fs = require('fs')
var split = require('split');
var _ = require('lodash')

var client = new es.Client({
  host: 'localhost:9200',
  keepAlive: false
});

var readStream = fs.createReadStream(process.argv[2]);
var stream = through(write)
var header;
var json;
var i = 0;

function write (data) {
  if (!header) makeHeader(data.toString());
  if (data.toString().length > 0) {
    json = _.zipObject(header, data.toString().split(','));
    upload(json)
  }
}

function makeHeader (data) {
  header = data.split(',').map(function(heading){ return '"' + heading + '"'});
}

function upload (object) {
  client.create({
    index: 'modis',
    type: 'type',
    id: i,
    body: object
  }, function (error, response) {
    if (error) {
      console.error(error);
      return;
    }
    if (response) {
      console.log('uploaded ' + JSON.stringify(response));
      return;
    }
  });
  i++;
}

readStream.pipe(split()).pipe(stream)
