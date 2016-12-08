'use strict';

var _ = require('lodash');
var hb = require('handlebars');

hb.registerHelper('lower', function(str) {
  return str.toLowerCase();
});

hb.registerHelper('cameltosnack', function(str) {
  return str.replace(/\.?([A-Z])/g, function (x,y){return "_" + y.toLowerCase()}).replace(/^_/, "");
});

hb.registerHelper('upper', function(str) {
  return str.toUpperCase();
});

hb.registerHelper('capitalize', function(str) {
  return _.capitalize(str);
});

module.exports = hb;
