'use strict';

var _ = require('lodash');

module.exports = {
  cameltosnack: cameltosnack
};

function cameltosnack(str) {
  return str.replace(/\.?([A-Z])/g, function (x,y){return "_" + y.toLowerCase()}).replace(/^_/, "");
}