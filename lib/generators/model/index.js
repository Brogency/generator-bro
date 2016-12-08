'use strict';

var _ = require('lodash');
var fs = require('fs');
var path = require('path');
var colors = require('colors');
var format = require('util').format;
var yeoman = require('yeoman-generator');
var f = require('../../utils/generateFilesStruct').f;
var helpers = require('../../core/helpers');
var core = require('../../core/generators/core');
var gHelper = require('../../core/generators/helper');

var selfGenerator = {
  _setArguments: function () {
    this.argument('appModelName', {
      desc: 'App name and model name in next format: app:ModelName',
      type: String, required: true
    });
  },

  _setOptions: function () {
    this.option('def-save', {
      alias: 's',
      desc: 'Create model method save for next overriding',
      type: Boolean, defaults: false});

    this.option('force', {
      alias: 'f',
      desc: 'Overwrite files that already exist',
      type: Boolean, defaults: false});

    this.option('prepopulated', {
      alias: 'p',
      desc: 'Prepopulated field name',
      type: String});

    this.option('model', {
      desc: 'File for model',
      type: String});

    this.option('admin', {
      desc: 'File for admin class',
      type: String});

    this.option('order', {
      alias: 'o',
      desc: 'Create field order, and add class Meta: ordering=("order", )',
      type: Boolean, defaults: false});
  },

  _afterInit: function () {
    var self = this;

    this.conflicter.force = this.options.force;

    // load model field types
    self.modelFieldTypes = self.fs.readJSON(
        self.templatePath('../model_field_types.json')
    );

    var appModelName = self.appModelName.split(':');

    if(appModelName.length !== 2) {
      self.log(colors.red('Error!') + ' First arg must be app name and models name in next format ' +
      colors.green('yo bro:model app:ModelName'));
      process.exit(1);
    }

    var fieldArgs = _.drop(self.arguments);

    self.appName = _.first(appModelName);
    self.modelName = _.last(appModelName);

    var fieldsObj = _.map(fieldArgs, getFieldObj);
    self.hasRedactorField = hasRedactorField(fieldArgs);
    self.fields = _.map(fieldsObj, serializeModelField);

    var fieldNames = _.pluck(fieldsObj, 'name');
    if (self.opts.prepopulated && fieldNames.indexOf(self.opts.prepopulated) === -1) {
      var formatObj = {
        error: colors.red('Error!'),
        prepopulated: colors.red(self.opts.prepopulated),
        fields: colors.green(fieldNames.join(', '))
      };
      console.log(f('{{error}} Option prepopulated is invalid, field ' +
      '{{prepopulated}} not found from self field: {{fields}}', formatObj));

      process.exit(1);
    }

    var isName = _.chain(fieldsObj)
        .find(where)
        .result('name', undefined)
        .value();

    self.prepopulated = self.opts.prepopulated || isName;
    self.order = self.opts.order;

    var isSlug = _.result(_.find(fieldsObj, 'name', 'slug'), 'name');

    self.isPrepopulated = isSlug && self.prepopulated;

    if(isSlug && !self.prepopulated) {
      self.warning(f('Finding slug field but prepopulated field not found.'));
    }

    self.isNameOrSlug = isName || isSlug;

    self.factoryFields = [];

    function where(f) {
      return f.name === 'name' || f.name === 'title';
    }

    function hasRedactorField(rawFields) {
      var result = false;

      _.each(rawFields, function(rawField) {
        var nameTypeArgs = rawField.split(':');
        var ftype = nameTypeArgs[1];
        if (ftype == 'redactor') {
          result = true;
        }
      });

      return result;
    }

    /**
     * Convert raw string to file object.
     *
     * Usage:
     *
     * var rawField = 'title:char:blank=True,null=True';
     * getFieldObj(rawField);
     * {name: 'title',
     *  args: {blank: True, null: True, max_length: 255, verbose_name: '_("Title")'},
     *  fieldType: 'models.CharField'}
     *
     * @param rawField
     * @returns {{name: *, args: Object, fieldType: *}}
     */
    function getFieldObj(rawField) {

      var validationErrMsg = colors.red('Error!') + f(' Field {{field}} invalid. ', {field: rawField}) +
          'Field must have next format: ' + colors.green('title:char:blank=True,null=True');

      var nameTypeArgs = rawField.split(':');

      if (nameTypeArgs.length !== 2 && nameTypeArgs.length !== 3) {
        console.log(validationErrMsg);
        process.exit(1);
      }

      var name = nameTypeArgs[0];
      var ftype = nameTypeArgs[1];
      var args = nameTypeArgs[2];

      var opts = getDefaultArgsForField(ftype, name); // options for field

      if (!opts) {
        console.log(colors.red(f('Error! Field {{name}} is not a valid. ' +
        'Enter valid django field.', {name: ftype})));
        process.exit(1);
      }

      if (args) {
        var listKeyVal = args.split(',');

        _.transform(listKeyVal, function (res, val){
          var keyVal = val.split('=');

          if (keyVal.length === 1) {
            res[keyVal[0]] = '';
          } else if(keyVal.length === 2) {
            res[keyVal[0]] = keyVal[1];
          } else {
            console.log(validationErrMsg);
            process.exit(1);
          }
        }, opts);
      }

      var fromModule = 'models.';
      if(ftype == 'redactor') {
        fromModule = ''
      }

      return {
        name: name,
        args: opts,
        fieldType: f('{{from}}{{ftype}}', {
          from: fromModule, ftype: self.modelFieldTypes[ftype].name})
      };

      /**
       * Get default args object for field initialize. Default args for field
       * must be set in file `model_field_types.json` for `field` param.
       * Default args building from two objects: model_field_types[field]
       * and `defaultArgsForAll` private variable.
       *
       * If field does not exist in model_field_types - return false.
       *
       * Will be removed in next minor version.
       *
       * @deprecated
       *
       * @private
       *
       * @param field {String}
       * @param name {String}
       * @returns {Object|Boolean}
       */
      function getDefaultArgsForField(field, name) {
        var defaultArgsForAll = {};  // jshint ignore:line

        if(!_.has(self.modelFieldTypes, field)) {
          return false;
        }

        var defaultArgsForself = self.modelFieldTypes[field].defaultArgs || {};

        return _.merge(defaultArgsForAll, defaultArgsForself);
      }
    }

    /**
     * Get string from object in django model field format.
     *
     * Usage:
     *
     * var field = {
     *  name: 'title',
     *  args: {max_length: 255, verbose_name: '_("Title")'},
     *  fieldType: 'models.CharField'};
     * serializeModelField(field);*
     * "title = models.CharField(
     *      max_length=255,
     *      verbose_name=_(\"Title\")
     *  )"
     *
     * @param field {Object}
     * @returns {String}
     */
    function serializeModelField(field) {
      field.opts = getOptions(field.args);
      if(field.opts != '') {
        return format('%s = %s(\n        %s\n    )', field.name, field.fieldType, field.opts);
      } else {
        return format('%s = %s()', field.name, field.fieldType);
      }

      /**
       * Get args and kwargs as string format for initializing
       * django model field. Sorting parameters begin args and then kwargs.
       *
       * Usage:
       *
       * var opts = {blank: True, null: True, News: ''};
       * getOptions(opts);
       * "\"News\", blank=True, null=True"
       *
       * @private
       *
       * @param args {Object}
       * @returns {String}
       */
      function getOptions(args) {
        var argsKwargs = _.chain(args)
            .map(getKeyVal).sortBy(sort).value();
        return argsKwargs.join(',\n        ');

        function getKeyVal(v, k) {
          return v? k + '=' + v : '"' + k + '"';
        }

        function sort(param, i) {
          return _.indexOf(param, '=') === -1 ? (i * -1) : i;
        }
      }
    }
  },

  _setContext: function () {
    return {
      app: path.join(this.config.get('apps'), this.appName),
      appsDir: this.config.get('pyApps'),
      defSave: this.opts.defSave,
      prepopulated: this.opts.prepopulated,
      force: this.opts.force,
      order: this.opts.order,
      model: this.opts.model,
      admin: this.opts.admin,
      appName: this.appName,
      modelName: this.modelName,
      fields: this.fields,
      isPrepopulated: this.isPrepopulated,
      hasRedactorField: this.hasRedactorField,
      isNameOrSlug: this.isNameOrSlug,
      factoryFields: this.factoryFields
    };
  },
  
  creating: {
    // models.py
    models: {
      src: '_model_item.py',
      dst: '{{app}}/models.py',
      isRun: function(self, src, dst) {
        return fs.existsSync(dst);
      },
      replacement: function(self, content, src, dst, context) {
        var modelCode = f(self.fs.read(src), context);
        return content + modelCode;
      }
    },

    // models/model_name.py
    modelNamed: {
      src: '_models.py',
      dst: '{{app}}/models/{{fileName}}.py',
      isRun: function(self, src, dst, context) {
        return fs.existsSync(
          self.destinationPath(f('{{app}}/models', context)));
      },
      replacement: function(self, content, src, dst, context) {
        var modelCode = f(self.fs.read(
          self.templatePath('_model_item.py')), context);
        return content + modelCode;
      },
      context: function(self) {
        return {
          fileName: (self.opts.model || self.modelName).toLowerCase()
        };
      }
    },

    // admin.py
    admin: {
      src: '_admin_item.py',
      dst: '{{app}}/admin.py',
      isRun: function(self, src, dst, context) {
        return fs.existsSync(dst);
      },
      replacement: function(self, content, src, dst, context) {
        var code = f(self.fs.read(src), context);
        return content + code;
      }
    },

    // admin/model_name.py
    adminNamed: {
      src: '_admin.py',
      dst: '{{app}}/admin/{{fileName}}.py',
      isRun: function(self, src, dst, context) {
        return fs.existsSync(f('{{app}}/admin', context));
      },
      replacement: function(self, content, src, dst, context) {
        var code = f(self.fs.read(
          self.templatePath('_admin_item.py')), context);
        return content + code;
      },
      context: function(self) {
        return {
          fileName: (self.opts.admin || self.modelName).toLowerCase()
        };
      }
    },

    // models/__init__.py
    modelInit: {
      dst: '{{app}}/models/__init__.py',
      isRun: function (self, src, dst) {
        return fs.existsSync(dst);
      },
      replacement: function(self, content) {
        var imports = [
          format('from apps.%s.models.%s import %s', self.appName,
            self.opts.model || self.modelName.toLowerCase(), self.modelName)
        ];
        return self.includeImports(imports, content);
      }
    },

    // admin/__init__.py
    adminInit: {
      dst: '{{app}}/admin/__init__.py',
      isRun: function (self, src, dst) {
        return fs.existsSync(dst);
      },
      replacement: function(self, content) {
        var imports = [
          format('from apps.%s.admin.%s import %sAdmin', self.appName,
            self.opts.admin || self.modelName.toLowerCase(), self.modelName)
        ];
        return self.includeImports(imports, content);
      }
    }
  },

  _afterEnd: function () {
    this.log(colors.green('Finish!') + ' Your models was created! Run ' +
      colors.green(f('./manage.py makemigrations {{appName}} && ./manage.py migrate', this)));
  }
};

module.exports = helpers.extendOf(gHelper, core, selfGenerator);
