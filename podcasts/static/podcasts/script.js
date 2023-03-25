if (window.location.pathname == '/podcasts/') {
    const buttons = document.querySelectorAll('.favorite');
    buttons.forEach(function(currentBtn){
        currentBtn.addEventListener('click', function() {
            favorite(currentBtn);
        });
    });
}

function favorite(btn) {
    btn.classList.replace("btn-outline-danger", "btn-danger");
}

// *******************
// DASHBOARD SCRIPTING
// *******************


function selectView() {
    const select = document.getElementById('dashboard');
    const view = select.value;
    window.location.href = `${view}/`
}
