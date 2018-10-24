/* global require */

if(window.jQuery){
  define('jquery', function(){
    return window.jQuery;
  });
}


require([
  'jquery',
  'video.converter-patterns-video'
  ], function($){
  'use strict';

  $(document).ready(function(){

    $('span.wcvideo a').each(function(){
      var $a = $(this);
      var $span = $a.parents('span.wcvideo');
      var width, height;
      if($span.hasClass('video-large')){
        width = 720;
        height = 480;
      }else if($span.hasClass('video-small')){
        width = 320;
        height = 240;
      }
      $.ajax({
        url: $a.attr('href') + '/@@video_macro',
        success: function(data){
          var $video = $(data);
          if(width && height){
            $video.find('[width]').attr('width', width);
            $video.find('[height]').attr('height', height);
          }
          $span.replaceWith($video);
          $video.find('video').mediaelementplayer({
            pluginPath: '++resource++video.converter-media/components/mediaelement/build/',
            features: ['playpause', 'current', 'progress', 'duration', 'tracks', 'volume', 'fullscreen',
                       'googleanalytics', 'universalgoogleanalytics']
          });
        }
      });
    });

  });

});
