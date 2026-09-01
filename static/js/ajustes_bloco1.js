// PontoCar — ajustes do bloco 1
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
      input.addEventListener('input', function () {
        input.value = input.value.toUpperCase();
      });
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
