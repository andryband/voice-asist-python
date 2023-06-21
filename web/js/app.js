let checkbox = document.getElementById('my-checkbox');
let image = document.getElementById('micr_img');
let modal = document.getElementById("myModal");
let btn = document.getElementById("info_btn");
let span = document.getElementsByClassName("close")[0];

function toggleLink() {
  var checkbox = document.getElementById('my-checkbox');
  var link = document.getElementById('setting-link');

  if (checkbox.checked) {
      link.classList.add('disabled');
      link.setAttribute('disabled', 'disabled');
  } else {
      link.classList.remove('disabled');
      link.removeAttribute('disabled');
  }
}

checkbox.addEventListener('change', function(){
    if(this.checked) {
        image.src = "img/micro-on.svg";
        toggleLink()
        eel.checkboxChanged(this.checked);
    } else {
        image.src = "img/micro-off.svg";
        toggleLink()
        eel.checkboxChanged(this.checked);
    }
});

function showModal() {
  modal.style.display = "block";
}
function closeModal() {
  modal.style.display = "none";
}

btn.onclick = showModal;
span.onclick = closeModal;
window.onclick = function(event) {
  if (event.target == modal) {
    closeModal();
  }
}


