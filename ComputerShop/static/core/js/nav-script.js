let catalog = document.querySelector('#catalog');
let dropdown = document.querySelector('#dropdown-cont');
let nav = document.querySelector('ul');


catalog.addEventListener('mouseover', handle);
catalog.addEventListener('mouseleave', handle2);

function handle() {
    nav.style.borderBottomLeftRadius = '0px';
    dropdown.style.borderTopLeftRadius = '0px';

    nav.style.transition = '0.2s';
}

function handle2() {

    
    nav.style.borderBottomLeftRadius = '38px';
    dropdown.style.borderTopLeftRadius = '38px';
    
    nav.style.transition = '0.2s';
}