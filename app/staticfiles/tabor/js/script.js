

let menutoggle = document.querySelector('.toggle');
let hammenu = document.querySelector('.hammenu');
menutoggle.onclick = function(){
    menutoggle.classList.toggle('active')
    hammenu.classList.toggle('active');
};


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
// audio
function play() {
var audio = document.getElementById('audio');
var audioicon = document.getElementById('audioicon');
if (audio.paused) {
audio.play();
$('#play').removeClass('glyphicon-play-circle')
$('#play').addClass('glyphicon-pause')
}else{
audio.pause();
audio.currentTime = 0
$('#play').addClass('glyphicon-play-circle')
$('#play').removeClass('glyphicon-pause')
};
};

// video
let videocontainer = document.querySelector('.video-container');
var uputavkaplay = document.getElementById('uputavka');
var zatvorBtn = document.getElementById('zatvor-btn');
var playvideo = document.getElementById('playvideo');
uputavkaplay.onclick = function(){
videocontainer.classList.toggle('active');
playvideo.currentTime = 0;
document.getElementById('playvideo').play();
};
zatvorBtn.onclick = function(){
videocontainer.classList.toggle('active');
document.getElementById('playvideo').pause();
};


// galéria

(function($) {
var list = $('.gallerylight');
var g2021btn = document.getElementById('g2021btn');
var gallery2021 = document.querySelector('.gallery2021');
var g2020btn = document.getElementById('g2020btn');
var gallery2020 = document.querySelector('.gallery2020');
var g2019btn = document.getElementById('g2019btn');
var gallery2019 = document.querySelector('.gallery2019');
var g2018btn = document.getElementById('g2018btn');
var gallery2018 = document.querySelector('.gallery2018');
var gallerylight = document.querySelector('gallerylight');
var zatvorgallery21 = document.querySelector('.zatvorgallery21');
var zatvorgallery20 = document.querySelector('.zatvorgallery20');
var zatvorgallery19 = document.querySelector('.zatvorgallery19');
var zatvorgallery18 = document.querySelector('.zatvorgallery18');
g2021btn.onclick = function(){
gallery2021.classList.toggle('active');
};
g2020btn.onclick = function(){
gallery2020.classList.toggle('active');
};
g2019btn.onclick = function(){
gallery2019.classList.toggle('active');
};
g2018btn.onclick = function(){
gallery2018.classList.toggle('active');
};
zatvorgallery21.onclick = function(){
console.log('zatvor');
gallery2021.classList.toggle('active');
};
zatvorgallery20.onclick = function(){
gallery2020.classList.toggle('active');
};
zatvorgallery19.onclick = function(){
gallery2019.classList.remove('active');
};
zatvorgallery18.onclick = function(){
gallery2018.classList.remove('active');
};



     
})(jQuery);

// postavičky

(function($) {
var otvorpostavicku = $('.nastim');
var zatvorpostavicku = $('.nastim');
otvorpostavicku.find('.postavicka');
zatvorpostavicku.find('zatvorpostavicku');
otvorpostavicku.find('.postavicka').on('click', function() {
$(this).addClass('active');
$(this).next().addClass('active');
});
zatvorpostavicku.find('.zatvorpostavicku').on('click', function() {
$(this).removeClass('active');
$(this).prev().removeClass('active');
});
})(jQuery);
