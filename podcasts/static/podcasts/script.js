// if (window.location.pathname == '/podcasts/') {
//     const buttons = document.querySelectorAll('.favorite');
//     buttons.forEach(function(currentBtn){
//         currentBtn.addEventListener('click', function() {
//             favorite(currentBtn);
//         });
//     });
// }

// function favorite(btn) {
//     btn.classList.replace("btn-outline-danger", "btn-danger");
// }

const app = {

    init: () => {
        document.addEventListener('DOMContentLoaded', app.load);
        console.log('HTML loaded');
    },

    load: () => {
        app.runScript();
    },

    runScript: () => {
        let page = document.getElementsByTagName('main');
        page = page[0].id;

        switch (page) {
            case 'podcasts':
                app.favoriteBtn();
            case 'video-main':
                app.ytContentScript();
            default:
                app.pass();
        }
    },

    pass: () => {
        return
    },


    // **********************
    // Content List Functions
    // **********************


    favorite: (btn) => {
        btn.classList.replace("btn-outline-danger", "btn-danger");
    },

    favoriteBtn: () => {
        const buttons = document.querySelectorAll('.favorite');
        buttons.forEach(function(currentBtn){
            currentBtn.addEventListener('click', function() {
                app.favorite(currentBtn);
            });
        });
    },


    // *************************
    // Youtube Content Functions
    // *************************


    // Outline what I need to do:
    //     Set up event listener to watch for a click on content items
    //     When clicked, retrieve the data-video-id attribute of the item
    //     And put that ID into the iframe player builder
    // I did all of this but this youtube iframe api stinks

    getVideoId: (e) => {
        let videoId = `${e.target.dataset.videoId}`;
        return videoId
    },

    callPlayer: (e) => {
        let videoId = app.getVideoId(e);
        let thumbnail = e.target;
        let parent = thumbnail.parentNode;
        let iframe = app.createIframe(videoId);
        iframe.classList.add("col-md-10");
        
        let tag = document.createElement('script');
        tag.src = "{% static 'podcasts/player.js' %}";
        let firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        parent.removeChild(thumbnail);
        parent.appendChild(iframe);
    },

    createIframe: (videoId) => {
        let iframe = document.createElement('iframe');
        iframe.setAttribute("id", "existing-iframe-example");
        iframe.setAttribute("width", "640");
        iframe.setAttribute("height", "360");
        iframe.setAttribute("src", `https://www.youtube.com/embed/${videoId}?enablejsapi=1`);
        iframe.setAttribute("frameborder", "0");
        iframe.setAttribute("style", "border: solid 4px #37474F");

        return iframe;
    },

    ytContentScript: () => {
        const main = document.querySelector("#video-main");

        main.addEventListener(
            "click",
            (event) => (app.callPlayer(event))
        );
    }
}
app.init();

// 2. This code loads the IFrame Player API code asynchronously.
let tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
let player;
function onYouTubeIframeAPIReady() {
player = new YT.Player('player', {
    height: '214',
    width: '192.5',
    videoId: "XweZnl6Xc3Y",
    playerVars: {
    'rel': 0,
    },
    events: {
    'onReady': onPlayerReady,
    'onStateChange': onPlayerStateChange
    }
});
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done = false;
function onPlayerStateChange(event) {
if (event.data == YT.PlayerState.PLAYING && !done) {
    setTimeout(stopVideo, 6000);
    done = true;
}
}
function stopVideo() {
player.stopVideo();
}