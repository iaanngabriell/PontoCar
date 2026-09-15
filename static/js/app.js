// PontoCar — interações compartilhadas
document.addEventListener('DOMContentLoaded', function () {

  // Menu mobile
  var burger = document.querySelector('.nav-burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    var accountLink = document.querySelector('.nav-actions > a.nav-link-plain');

    function syncMobileAccountLink() {
      var existing = links.querySelector('.nav-mobile-account-link');
      if (window.innerWidth <= 980 && accountLink) {
        if (!existing) {
          var clone = accountLink.cloneNode(true);
          clone.classList.remove('nav-link-plain');
          clone.classList.add('nav-mobile-account-link');
          clone.addEventListener('click', function () { setMenu(false); });
          links.appendChild(clone);
        }
      } else if (existing) {
        existing.remove();
      }
    }

    function setMenu(open) {
      links.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    }

    syncMobileAccountLink();

    burger.addEventListener('click', function () {
      setMenu(!links.classList.contains('is-open'));
    });

    links.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setMenu(false); });
    });

    document.addEventListener('click', function (event) {
      if (!links.classList.contains('is-open')) return;
      if (links.contains(event.target) || burger.contains(event.target)) return;
      setMenu(false);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') setMenu(false);
    });

    window.addEventListener('resize', function () {
      syncMobileAccountLink();
      if (window.innerWidth > 980) setMenu(false);
    });
  }

  // Selects modernos. Mantém o <select> real no formulário e apenas melhora a interface.
  if (typeof window.TomSelect !== 'undefined') {
    document.querySelectorAll('select:not([data-native-select])').forEach(function (select) {
      if (select.tomselect) return;

      var config = {
        create: false,
        allowEmptyOption: true,
        closeAfterSelect: !select.multiple,
        maxOptions: null,
        hideSelected: false,
        plugins: select.multiple ? ['remove_button'] : [],
        render: {
          no_results: function () {
            return '<div class="no-results">Nenhuma opção encontrada</div>';
          }
        }
      };

      // Listas curtas continuam simples; listas maiores ganham busca por digitação.
      if (!select.multiple && select.options.length <= 7) {
        config.controlInput = null;
      }

      new window.TomSelect(select, config);
    });
  }

  // Inputs de arquivo com botão e nome do arquivo separados.
  document.querySelectorAll('input[type="file"]:not([hidden])').forEach(function (input, index) {
    if (input.dataset.pcFileEnhanced === 'true') return;
    input.dataset.pcFileEnhanced = 'true';

    if (!input.id) input.id = 'pc-file-input-' + index;

    var wrapper = document.createElement('div');
    wrapper.className = 'pc-file-picker';

    input.parentNode.insertBefore(wrapper, input);
    wrapper.appendChild(input);
    input.classList.add('pc-file-picker-input');

    var trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'pc-file-picker-trigger';
    trigger.textContent = input.multiple ? 'Escolher arquivos' : 'Escolher arquivo';
    trigger.setAttribute('aria-controls', input.id);
    trigger.disabled = input.disabled;

    var filename = document.createElement('span');
    filename.className = 'pc-file-picker-name';
    filename.textContent = 'Nenhum arquivo selecionado';
    filename.setAttribute('aria-live', 'polite');

    wrapper.appendChild(trigger);
    wrapper.appendChild(filename);

    trigger.addEventListener('click', function () {
      input.click();
    });

    input.addEventListener('change', function () {
      var files = Array.from(input.files || []);
      if (!files.length) {
        filename.textContent = 'Nenhum arquivo selecionado';
      } else if (files.length === 1) {
        filename.textContent = files[0].name;
      } else {
        filename.textContent = files.length + ' arquivos selecionados';
      }
      wrapper.classList.toggle('has-file', files.length > 0);
    });
  });

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

  // Preview de upload de fotos (formulário de veículo).
  // Mantém o input sincronizado quando uma miniatura é removida.
  var uploadInput = document.querySelector('#foto-upload');
  var photoGrid = document.querySelector('#photo-grid');
  if (uploadInput && photoGrid) {
    var selectedFiles = [];

    function syncInput() {
      if (typeof DataTransfer === 'undefined') return;
      var transfer = new DataTransfer();
      selectedFiles.forEach(function (file) { transfer.items.add(file); });
      uploadInput.files = transfer.files;
    }

    function renderPhotos() {
      photoGrid.innerHTML = '';
      selectedFiles.forEach(function (file, index) {
        var reader = new FileReader();
        reader.onload = function (e) {
          var div = document.createElement('div');
          div.className = 'photo-thumb';
          div.innerHTML = '<img src="' + e.target.result + '" alt="Foto do veículo"><button class="remove" type="button" aria-label="Remover foto"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button>';
          div.querySelector('.remove').addEventListener('click', function () {
            selectedFiles.splice(index, 1);
            syncInput();
            renderPhotos();
          });
          photoGrid.appendChild(div);
        };
        reader.readAsDataURL(file);
      });
    }

    uploadInput.addEventListener('change', function () {
      selectedFiles = Array.from(uploadInput.files).slice(0, 8);
      syncInput();
      renderPhotos();
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
