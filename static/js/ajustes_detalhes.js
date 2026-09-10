(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var mainImage = document.getElementById('vehicle-main-image');
    if (!mainImage) return;

    document.querySelectorAll('.gallery-thumb-button').forEach(function (button) {
      button.addEventListener('click', function () {
        var src = button.getAttribute('data-gallery-src');
        var alt = button.getAttribute('data-gallery-alt') || '';
        if (!src) return;

        mainImage.src = src;
        mainImage.alt = alt;
        document.querySelectorAll('.gallery-thumb-button').forEach(function (item) {
          item.classList.remove('active');
        });
        button.classList.add('active');
      });
    });
  });
})();
