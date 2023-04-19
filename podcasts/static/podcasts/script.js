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
}