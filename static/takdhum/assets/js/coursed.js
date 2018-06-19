;(function ($) {
  $(window).load(function () {
    var accHeight = $('#accordion').height()
    var vw = $(window).width()
    $('#videoDisplay').css(
      'min-height',
      Math.min(vw < 640 ? 0 : vw, accHeight)
    )

    $('#accordion .list-video').each(function () {
      var self = $(this)
      if (!self.data('link')) return
      self.on('click', function () {
        var self = $(this)
        $('#videoDisplay').html(
          '<div class="embed-responsive embed-responsive-16by9">' +
            '<iframe class="embed-responsive-item "allowfullscreen src="' +
            self.data('link') +
            '"></iframe>' +
            '</div>'
        )
        $.post('http://127.0.0.1:8000/api/stats', {video: self.data('link')})
        .done(function () {
            console.log('Successfully sent analytics data')
        })
        .fail(function () {
            console.warn('Analytics request failed!')
        })
      })
    })
  })
})(window.jQuery)
