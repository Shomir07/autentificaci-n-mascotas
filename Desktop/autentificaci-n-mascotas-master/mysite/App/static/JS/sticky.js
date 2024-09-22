document.addEventListener('DOMContentLoaded', function() {
  const closeIcon = document.querySelector('.cross-icon');
  const stickyNote = document.querySelector('.sticky-note');

  // Verificar el estado del sticky note
  if (!sessionStorage.getItem('stickyNoteClosed')) {
    // Mostrar el sticky note si no está marcado como cerrado
    stickyNote.classList.add('show');
  } else {
    // No mostrar el sticky note si está marcado como cerrado
    stickyNote.classList.remove('show');
  }

  // Manejar el clic en el icono de cerrar
  if (closeIcon && stickyNote) {
    closeIcon.addEventListener('click', function() {
      stickyNote.classList.remove('show');
      // Guardar en sessionStorage para recordar que se cerró en esta sesión
      sessionStorage.setItem('stickyNoteClosed', 'true');
    });
  }

  // Limpiar el estado del sticky note cuando se inicia una nueva sesión (nueva ventana o pestaña)
  window.addEventListener('load', function() {
    // Verificar si se está cargando en una nueva sesión
    if (!sessionStorage.getItem('sessionStarted')) {
      sessionStorage.setItem('sessionStarted', 'true');
      sessionStorage.removeItem('stickyNoteClosed'); // Eliminar la marca de cerrado para mostrar el sticky note en una nueva sesión
    }
  });

  // Limpiar el estado de la sesión al cerrar la página o el navegador
  window.addEventListener('beforeunload', function() {
    sessionStorage.removeItem('sessionStarted'); // Eliminar la marca de sesión para permitir la visualización en la próxima sesión
  });
});
