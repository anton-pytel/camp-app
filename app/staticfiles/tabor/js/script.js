
            let nastimobal = document.querySelector('.nastimobal');
            var nastimclick = document.getElementById('nastimobal');
            var nastimclickz = document.getElementById('nastimobalz');
            nastimclick.onclick = function(){
            nastimobal.classList.toggle('active');
        };
            nastimclickz.onclick = function(){
                nastimobal.classList.remove('active');
            };
        

            (function($) {
                var list = $('.info4');
                list.find('dd').hide();

                list.find('dt').on('click', function() {
                    $(this).next().slideToggle()
                            .siblings('dd').slideUp();
                });
            })(jQuery);

            function play() {
        var audio = document.getElementById('audio');
        if (audio.paused) {
            audio.play();
            $('#play').removeClass('glyphicon-play-circle')
            $('#play').addClass('glyphicon-pause')
        }else{
            audio.pause();
            audio.currentTime = 0
            $('#play').addClass('glyphicon-play-circle')
            $('#play').removeClass('glyphicon-pause')
        }
    }

    function playvideo() {
        var video = document.getElementById('uputavka');
        if (video.paused) {
            video.play();
            $('#uputavka').removeClass('glyphicon-play-circle')
            $('#uputavka').addClass('glyphicon-pause')
        }else{
            video.pause();
            video.currentTime = 0
            $('#uputavka').addClass('glyphicon-play-circle')
            $('#uputavka').removeClass('glyphicon-pause')
        }
    }
