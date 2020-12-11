$(document).ready(function() {
    $('.subscribe .post-list .check').on('click', function() {
        var self = this;
        var date = $(this).attr("date");

        $.ajax({
            type: "POST",
            url: window.location.href,
            data: {date: date},
            success: function(last_seen) {
                if (last_seen == date) {
                    $(self).closest('.post').nextAll().addClass('disable');
                    $(self).closest('.post').addClass('disable');
                }
            }
        });
    });

    $('.subscribe .post-list .favorite').on('click', function() {
        var self = this;

        $.ajax({
            type: "POST",
            url: window.location.href + "favorite/",
            data: {post_id: $(this).attr("post_id")},
            success: function(msg) {
                if (msg == 'added') {
                    $(self).addClass('active');
                } else {
                    $(self).removeClass('active');
                }
            }
        });
    });

    $('.subscribe .mark-all').on('click', function() {
        $('.subscribe .post-list .check').last().trigger('click');

        window.scrollTo(0, 0);
    });
});
