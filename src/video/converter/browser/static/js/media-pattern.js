/* global define */
define([
  'jquery',
  'mockup-patterns-base',
  'mediaelement',
  'mep-feature-googleanalytics',
  'mep-feature-quality',
  'mep-feature-universalgoogleanalytics'
], function($, Base) {
  'use strict';

  var Media = Base.extend({
    name: 'media',
    trigger: '.pat-media',
    defaults: {
    },
    init: function() {
      var self = this;
      self.$el.mediaelementplayer({
        pluginPath: '++resource++video.converter/components/mediaelement/build/',
        features: ['playpause','current','progress','duration','tracks','volume','fullscreen',
                   'googleanalytics', 'universalgoogleanalytics', 'quality']
      });
    }
  });

  return Media;

});
