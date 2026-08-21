// AutoPalmas — interações compartilhadas
document.addEventListener('DOMContentLoaded', function () {

  // Menu mobile
  var burger = document.querySelector('.nav-burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      var open = links.style.display === 'flex';
      links.style.display = open ? 'none' : 'flex';
      links.style.flexDirection = 'column';
      links.style.position = 'absolute';
      links.style.top = '76px';
      links.style.left = '0';
      links.style.right = '0';
      links.style.background = '#0a1626';
      links.style.padding = '18px 24px';
      links.style.gap = '16px';
    });
  }

  // Galeria de fotos (página de detalhes do veículo)
  var mainPhoto = document.querySelector('.gallery-main img');
  document.querySelectorAll('.gallery-thumbs img').forEach(function (thumb) {
    thumb.addEventListener('click', function () {
      document.querySelectorAll('.gallery-thumbs img').forEach(function (t) { t.classList.remove('active'); });
      thumb.classList.add('active');
      if (mainPhoto) mainPhoto.src = thumb.src;
    });
  });

  // Tabs simples (troca de painel por data-tab)
  document.querySelectorAll('[data-tabs] .tabs a').forEach(function (tabLink) {
    tabLink.addEventListener('click', function (e) {
      var group = tabLink.closest('[data-tabs]');
      if (!group.querySelector('[data-tab-panel]')) return; // sem painéis JS, navegação normal
      e.preventDefault();
      group.querySelectorAll('.tabs a').forEach(function (a) { a.classList.remove('active'); });
      tabLink.classList.add('active');
      var target = tabLink.getAttribute('data-target');
      group.querySelectorAll('[data-tab-panel]').forEach(function (panel) {
        panel.style.display = (panel.getAttribute('data-tab-panel') === target) ? 'block' : 'none';
      });
    });
  });

  // Favoritar (toggle visual)
  document.querySelectorAll('.fav').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      btn.classList.toggle('active');
      btn.style.color = btn.classList.contains('active') ? '#3ebd52' : '#fff';
    });
  });

  // Preview de upload de fotos (formulário de veículo)
  var uploadInput = document.querySelector('#foto-upload');
  var photoGrid = document.querySelector('#photo-grid');
  if (uploadInput && photoGrid) {
    uploadInput.addEventListener('change', function () {
      Array.from(uploadInput.files).forEach(function (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
          var div = document.createElement('div');
          div.className = 'photo-thumb';
          div.innerHTML = '<img src="' + e.target.result + '" alt="Foto do veículo"><button class="remove" type="button" aria-label="Remover foto"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>';
          div.querySelector('.remove').addEventListener('click', function () { div.remove(); });
          photoGrid.appendChild(div);
        };
        reader.readAsDataURL(file);
      });
    });
  }

  // Range de preço — atualiza label
  var priceRange = document.querySelector('#preco-max');
  var priceLabel = document.querySelector('#preco-max-label');
  if (priceRange && priceLabel) {
    priceRange.addEventListener('input', function () {
      priceLabel.textContent = 'Até R$ ' + Number(priceRange.value).toLocaleString('pt-BR');
    });
  }
});
