// JS global pour interactions simples (ex: alert Panier vide etc.)
document.addEventListener('DOMContentLoaded', function() {
  // Exemple : liens avec data-confirm
  document.querySelectorAll('[data-confirm]').forEach(function(el){
    el.addEventListener('click', function(e){
      if(!confirm(el.getAttribute('data-confirm'))) e.preventDefault();
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const mobileSearch = document.getElementById("mobileSearch");
  const mobileSearchBtn = document.getElementById("mobileSearchBtn");
  const closeSearch = document.getElementById("closeSearch");

  if (mobileSearchBtn) {
    mobileSearchBtn.addEventListener("click", () => mobileSearch.classList.add("active"));
  }
  if (closeSearch) {
    closeSearch.addEventListener("click", () => mobileSearch.classList.remove("active"));
  }
});
