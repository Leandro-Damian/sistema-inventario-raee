// Utilidades livianas del sistema (sin dependencias externas).
document.addEventListener('DOMContentLoaded', function () {
  // Cerrar avisos luego de unos segundos sin impedir la impresión.
  document.querySelectorAll('[data-auto-dismiss]').forEach(function (el) {
    setTimeout(function () { el.style.display = 'none'; }, 6000);
  });

  // Confirmación para acciones destructivas explícitamente marcadas.
  document.querySelectorAll('form[data-confirm]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      if (!window.confirm(form.getAttribute('data-confirm'))) event.preventDefault();
    });
  });
});
