(function () {
  'use strict';

  var MAX_PHOTOS = 8;
  var MAX_BYTES = 8 * 1024 * 1024;
  var ACCEPTED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

  function getCsrfToken() {
    var input = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return input ? input.value : '';
  }

  function updateTileLabels(grid) {
    if (!grid) return;
    var tiles = Array.from(grid.querySelectorAll('.vehicle-photo-tile'));
    tiles.forEach(function (tile, index) {
      var number = tile.querySelector('.vehicle-photo-order-number');
      var cover = tile.querySelector('.vehicle-photo-cover-label');
      if (number) number.textContent = String(index + 1);
      if (cover) cover.textContent = index === 0 ? 'Capa' : 'Foto';

      var previous = tile.querySelector('[data-direction="-1"]');
      var next = tile.querySelector('[data-direction="1"]');
      if (previous) previous.disabled = index === 0;
      if (next) next.disabled = index === tiles.length - 1;
    });
  }

  function moveDomTile(tile, direction) {
    if (!tile || !tile.parentElement) return false;
    var grid = tile.parentElement;
    if (direction < 0) {
      var previous = tile.previousElementSibling;
      if (!previous) return false;
      grid.insertBefore(tile, previous);
      return true;
    }
    var next = tile.nextElementSibling;
    if (!next) return false;
    grid.insertBefore(next, tile);
    return true;
  }

  function enableExistingPhotoOrder() {
    var grid = document.getElementById('existing-photo-grid');
    if (!grid) return;

    var status = document.getElementById('existing-photo-order-status');
    var reorderUrl = grid.getAttribute('data-reorder-url');
    var dragged = null;
    var saveTimer = null;

    function setStatus(message, className) {
      if (!status) return;
      status.textContent = message || '';
      status.className = 'vehicle-photo-save-status' + (className ? ' ' + className : '');
    }

    function currentOrder() {
      return Array.from(grid.querySelectorAll('[data-existing-photo-id]')).map(function (tile) {
        return tile.getAttribute('data-existing-photo-id');
      });
    }

    function saveOrder() {
      if (!reorderUrl) return;
      setStatus('Salvando ordem…', 'is-saving');

      fetch(reorderUrl, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCsrfToken(),
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ ordem: currentOrder() })
      })
        .then(function (response) {
          return response.json().then(function (payload) {
            if (!response.ok || !payload.ok) {
              throw new Error(payload.erro || 'Não foi possível salvar a ordem.');
            }
            return payload;
          });
        })
        .then(function () {
          setStatus('Ordem salva.', 'is-success');
          window.setTimeout(function () {
            if (status && status.classList.contains('is-success')) setStatus('');
          }, 2200);
        })
        .catch(function (error) {
          setStatus(error.message || 'Erro ao salvar a ordem.', 'is-error');
        });
    }

    function queueSave() {
      updateTileLabels(grid);
      if (saveTimer) window.clearTimeout(saveTimer);
      saveTimer = window.setTimeout(saveOrder, 180);
    }

    grid.addEventListener('click', function (event) {
      var button = event.target.closest('.vehicle-photo-move');
      if (!button) return;
      var tile = button.closest('.vehicle-photo-tile');
      var direction = Number(button.getAttribute('data-direction'));
      if (moveDomTile(tile, direction)) queueSave();
    });

    grid.addEventListener('dragstart', function (event) {
      var tile = event.target.closest('.vehicle-photo-tile');
      if (!tile) return;
      dragged = tile;
      tile.classList.add('is-dragging');
      if (event.dataTransfer) {
        event.dataTransfer.effectAllowed = 'move';
        event.dataTransfer.setData('text/plain', tile.getAttribute('data-existing-photo-id') || 'photo');
      }
    });

    grid.addEventListener('dragover', function (event) {
      event.preventDefault();
      var target = event.target.closest('.vehicle-photo-tile');
      grid.querySelectorAll('.is-drop-target').forEach(function (tile) {
        if (tile !== target) tile.classList.remove('is-drop-target');
      });
      if (target && target !== dragged) target.classList.add('is-drop-target');
    });

    grid.addEventListener('drop', function (event) {
      event.preventDefault();
      var target = event.target.closest('.vehicle-photo-tile');
      if (!dragged || !target || dragged === target) return;

      var rect = target.getBoundingClientRect();
      var insertAfter = event.clientX > rect.left + rect.width / 2;
      if (insertAfter) {
        target.insertAdjacentElement('afterend', dragged);
      } else {
        target.insertAdjacentElement('beforebegin', dragged);
      }
      queueSave();
    });

    grid.addEventListener('dragend', function () {
      grid.querySelectorAll('.vehicle-photo-tile').forEach(function (tile) {
        tile.classList.remove('is-dragging', 'is-drop-target');
      });
      dragged = null;
    });

    updateTileLabels(grid);
  }

  function enableNewPhotoSelection() {
    var input = document.getElementById('vehicle-foto-upload');
    var grid = document.getElementById('vehicle-new-photo-grid');
    var feedback = document.getElementById('vehicle-new-photo-feedback');
    if (!input || !grid) return;

    var existingGrid = document.getElementById('existing-photo-grid');
    var existingCount = existingGrid ? existingGrid.querySelectorAll('.vehicle-photo-tile').length : 0;
    var maxNewPhotos = Math.max(0, MAX_PHOTOS - existingCount);
    var selectedFiles = [];
    var previewUrls = new Map();
    var draggedIndex = null;

    function setFeedback(message, isError) {
      if (!feedback) return;
      feedback.textContent = message || '';
      feedback.className = 'vehicle-photo-feedback' + (isError ? ' is-error' : '');
    }

    function fileKey(file) {
      return [file.name, file.size, file.lastModified].join('::');
    }

    function syncInput() {
      if (typeof DataTransfer === 'undefined') return;
      var transfer = new DataTransfer();
      selectedFiles.forEach(function (file) {
        transfer.items.add(file);
      });
      input.files = transfer.files;
    }

    function getPreviewUrl(file) {
      if (!previewUrls.has(file)) {
        previewUrls.set(file, URL.createObjectURL(file));
      }
      return previewUrls.get(file);
    }

    function removeFile(index) {
      var removed = selectedFiles[index];
      if (removed && previewUrls.has(removed)) {
        URL.revokeObjectURL(previewUrls.get(removed));
        previewUrls.delete(removed);
      }
      selectedFiles.splice(index, 1);
      syncInput();
      render();
    }

    function moveFile(index, direction) {
      var target = index + direction;
      if (target < 0 || target >= selectedFiles.length) return;
      var file = selectedFiles.splice(index, 1)[0];
      selectedFiles.splice(target, 0, file);
      syncInput();
      render();
    }

    function render() {
      grid.innerHTML = '';

      selectedFiles.forEach(function (file, index) {
        var tile = document.createElement('article');
        tile.className = 'vehicle-photo-tile';
        tile.draggable = true;
        tile.setAttribute('data-new-photo-index', String(index));

        var img = document.createElement('img');
        img.src = getPreviewUrl(file);
        img.alt = 'Prévia da foto ' + (index + 1) + ' do veículo';
        tile.appendChild(img);

        var topbar = document.createElement('div');
        topbar.className = 'vehicle-photo-topbar';
        topbar.innerHTML = '<span class="vehicle-photo-cover-label">' + (index === 0 && existingCount === 0 ? 'Capa' : 'Foto') + '</span><span class="vehicle-photo-drag-label" title="Arraste para reordenar">⋮⋮</span>';
        tile.appendChild(topbar);

        var remove = document.createElement('button');
        remove.type = 'button';
        remove.className = 'vehicle-photo-remove';
        remove.setAttribute('aria-label', 'Remover foto');
        remove.textContent = '×';
        remove.addEventListener('click', function () { removeFile(index); });
        tile.appendChild(remove);

        var bottombar = document.createElement('div');
        bottombar.className = 'vehicle-photo-bottombar';
        bottombar.innerHTML = '<span class="vehicle-photo-order-number">' + (existingCount + index + 1) + '</span><div class="vehicle-photo-order-actions"><button type="button" class="vehicle-photo-move" data-direction="-1" aria-label="Mover foto para a esquerda">←</button><button type="button" class="vehicle-photo-move" data-direction="1" aria-label="Mover foto para a direita">→</button></div>';
        tile.appendChild(bottombar);

        var moveButtons = tile.querySelectorAll('.vehicle-photo-move');
        moveButtons[0].disabled = index === 0;
        moveButtons[1].disabled = index === selectedFiles.length - 1;
        moveButtons.forEach(function (button) {
          button.addEventListener('click', function () {
            moveFile(index, Number(button.getAttribute('data-direction')));
          });
        });

        tile.addEventListener('dragstart', function (event) {
          draggedIndex = index;
          tile.classList.add('is-dragging');
          if (event.dataTransfer) {
            event.dataTransfer.effectAllowed = 'move';
            event.dataTransfer.setData('text/plain', String(index));
          }
        });

        tile.addEventListener('dragover', function (event) {
          event.preventDefault();
          if (draggedIndex !== null && draggedIndex !== index) tile.classList.add('is-drop-target');
        });

        tile.addEventListener('dragleave', function () {
          tile.classList.remove('is-drop-target');
        });

        tile.addEventListener('drop', function (event) {
          event.preventDefault();
          tile.classList.remove('is-drop-target');
          if (draggedIndex === null || draggedIndex === index) return;

          var moved = selectedFiles.splice(draggedIndex, 1)[0];
          var targetIndex = index;
          if (draggedIndex < index) targetIndex -= 1;

          var rect = tile.getBoundingClientRect();
          if (event.clientX > rect.left + rect.width / 2) targetIndex += 1;
          selectedFiles.splice(Math.max(0, Math.min(targetIndex, selectedFiles.length)), 0, moved);
          draggedIndex = null;
          syncInput();
          render();
        });

        tile.addEventListener('dragend', function () {
          draggedIndex = null;
          grid.querySelectorAll('.vehicle-photo-tile').forEach(function (item) {
            item.classList.remove('is-dragging', 'is-drop-target');
          });
        });

        grid.appendChild(tile);
      });

      if (selectedFiles.length) {
        setFeedback(selectedFiles.length + ' nova' + (selectedFiles.length === 1 ? ' foto selecionada.' : 's fotos selecionadas.'), false);
      } else {
        setFeedback('', false);
      }
    }

    input.addEventListener('change', function () {
      var incoming = Array.from(input.files || []);
      var known = new Set(selectedFiles.map(fileKey));
      var errors = [];

      incoming.forEach(function (file) {
        if (known.has(fileKey(file))) return;
        if (file.size > MAX_BYTES) {
          errors.push(file.name + ' excede 8 MB.');
          return;
        }
        if (file.type && ACCEPTED_TYPES.indexOf(file.type) === -1) {
          errors.push(file.name + ' não é JPEG, PNG ou WebP.');
          return;
        }
        if (selectedFiles.length >= maxNewPhotos) {
          errors.push('O veículo pode ter no máximo ' + MAX_PHOTOS + ' fotos.');
          return;
        }
        selectedFiles.push(file);
        known.add(fileKey(file));
      });

      syncInput();
      render();
      if (errors.length) setFeedback(errors.join(' '), true);
    });

    if (maxNewPhotos === 0) {
      input.disabled = true;
      var label = document.querySelector('label[for="vehicle-foto-upload"]');
      if (label) {
        label.setAttribute('aria-disabled', 'true');
        label.classList.add('is-disabled');
      }
      setFeedback('O veículo já possui o limite de 8 fotos. Reordene as fotos cadastradas.', false);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    enableExistingPhotoOrder();
    enableNewPhotoSelection();
  });
})();
