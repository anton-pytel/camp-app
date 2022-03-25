let nastimobal = document.querySelector('.nastimobal');
var nastimclick = document.getElementById('nastimobal');
var nastimclickz = document.getElementById('nastimobalz');
nastimclick.onclick = function () {

    nastimobal.classList.toggle('active');
};
nastimclickz.onclick = function () {
    nastimobal.classList.remove('active');
};


(function ($) {
    var list = $('.info4');
    list.find('dd').hide();

    list.find('dt').on('click', function () {
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
    } else {
        audio.pause();
        audio.currentTime = 0
        $('#play').addClass('glyphicon-play-circle')
        $('#play').removeClass('glyphicon-pause')
    }
}

let videocontainer = document.querySelector('.video-container');
var uputavkaplay = document.getElementById('uputavka');
var zatvorBtn = document.getElementById('zatvor-btn');
var playvideo = document.getElementById('playvideo');
uputavkaplay.onclick = function () {
    videocontainer.classList.toggle('active');
    playvideo.currentTime = 0;
    document.getElementById('playvideo').play();
};
zatvorBtn.onclick = function () {
    videocontainer.classList.toggle('active');
    document.getElementById('playvideo').pause();
};