var view=0;
function toggleUp(element) {
    if(element.className.indexOf('bi-arrow-up-square')!==-1){
        element.classList.add("bi-arrow-up-square-fill");
        element.classList.remove("bi-arrow-up-square");
    }
}

function toggleDown(element) {
    if(element.className.indexOf('bi-arrow-down-square')!==-1){
        element.classList.remove("bi-arrow-down-square");
        element.classList.add("bi-arrow-down-square-fill");
    }
}

function toggleView(element){
    if(view===0){
        view=1;
        document.getElementById('containerGraph').style.display='none';
        document.getElementById('containerComments').style.display='block';
        element.classList.remove("bi-toggle2-off");
        element.classList.add("bi-toggle2-on");
    }
    else{
        view=0;
        document.getElementById('containerGraph').style.display='block';
        document.getElementById('containerComments').style.display='none';
        element.classList.remove("bi-toggle2-on");
        element.classList.add("bi-toggle2-off");
    }
}