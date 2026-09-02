// PontoCar — máscaras, normalizações visuais e formatação de campos
(function () {
  'use strict';

  function onlyDigits(value) {
    return (value || '').replace(/\D/g, '');
  }

  function formatCPF(value) {
    var d = onlyDigits(value).slice(0, 11);
    d = d.replace(/(\d{3})(\d)/, '$1.$2');
    d = d.replace(/(\d{3})(\d)/, '$1.$2');
    d = d.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    return d;
  }

  function formatCNPJ(value) {
    var d = onlyDigits(value).slice(0, 14);
    d = d.replace(/^(\d{2})(\d)/, '$1.$2');
    d = d.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
    d = d.replace(/\.(\d{3})(\d)/, '.$1/$2');
    d = d.replace(/(\d{4})(\d)/, '$1-$2');
    return d;
  }

  function formatCEP(value) {
    var d = onlyDigits(value).slice(0, 8);
    return d.replace(/(\d{5})(\d)/, '$1-$2');
  }

  function formatTelefone(value) {
    var d = onlyDigits(value).slice(0, 11);
    if (d.length <= 10) {
      d = d.replace(/^(\d{2})(\d)/, '($1) $2');
      d = d.replace(/(\d{4})(\d)/, '$1-$2');
    } else {
      d = d.replace(/^(\d{2})(\d)/, '($1) $2');
      d = d.replace(/(\d{5})(\d)/, '$1-$2');
    }
    return d;
  }

  function parseMoneyBR(value) {
    var text = (value || '')
      .replace(/R\$/gi, '')
      .replace(/\s/g, '')
      .trim();

    if (!text) return null;

    // Quando há vírgula, tratamos ponto como milhar.
    if (text.indexOf(',') !== -1) {
      text = text.replace(/\./g, '').replace(',', '.');
    } else if (/^-?\d{1,3}(\.\d{3})+$/.test(text)) {
      text = text.replace(/\./g, '');
    }

    var number = Number(text);
    return Number.isFinite(number) ? number : null;
  }

  function formatMoneyBR(value) {
    var number = parseMoneyBR(value);
    if (number === null) return value || '';
    return number.toLocaleString('pt-BR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-mask]').forEach(function (input) {
      function applyMask() {
        var type = input.getAttribute('data-mask');
        if (type === 'cpf') input.value = formatCPF(input.value);
        if (type === 'cnpj') input.value = formatCNPJ(input.value);
        if (type === 'cep') input.value = formatCEP(input.value);
        if (type === 'telefone') input.value = formatTelefone(input.value);
      }
      input.addEventListener('input', applyMask);
      applyMask();
    });

    document.querySelectorAll('[data-uppercase]').forEach(function (input) {
      function upper() {
        input.value = input.value.toUpperCase();
      }
      input.addEventListener('input', upper);
      upper();
    });

    document.querySelectorAll('[data-money="brl"]').forEach(function (input) {
      function formatOnBlur() {
        if (input.value.trim()) input.value = formatMoneyBR(input.value);
      }

      input.addEventListener('blur', formatOnBlur);
      formatOnBlur();
    });

    document.querySelectorAll('[data-description-counter]').forEach(function (textarea) {
      var max = Number(textarea.getAttribute('maxlength')) || 0;
      if (!max) return;

      var counter = document.createElement('div');
      counter.className = 'description-counter';
      textarea.insertAdjacentElement('afterend', counter);

      function refreshCounter() {
        counter.textContent = textarea.value.length + ' / ' + max + ' caracteres';
      }
      textarea.addEventListener('input', refreshCounter);
      refreshCounter();
    });

    var roleCards = document.querySelectorAll('.role-card');
    function refreshRoleCards() {
      roleCards.forEach(function (card) {
        var radio = card.querySelector('input[type="radio"]');
        card.classList.toggle('is-selected', !!(radio && radio.checked));
      });
    }
    roleCards.forEach(function (card) {
      var radio = card.querySelector('input[type="radio"]');
      if (radio) radio.addEventListener('change', refreshRoleCards);
    });
    refreshRoleCards();
  });
})();
