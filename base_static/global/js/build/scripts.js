const changeDisplayStyle = (element, display) => {
  if (element) element.style.display = display;
}

const addClassList = (element, value) => {
  if (element) element.classList.add(value);
}

const removeClassList = (element, value) => {
  if (element) element.classList.remove(value);
}

(() => {
  const hamburguerMenu = document.querySelector('#menu-hamburguer');
  const closeMenuIcon = document.querySelector('#close-menu');
  const sidebar = document.querySelector('.sidebar');
  const fadeInClass = 'fade-in';

  if (!hamburguerMenu || !closeMenuIcon || !sidebar) return;

  const showMenu = () => {
    addClassList(sidebar, fadeInClass);
    changeDisplayStyle(sidebar, 'flex');
    changeDisplayStyle(hamburguerMenu, 'none');
    changeDisplayStyle(closeMenuIcon, 'block');
  };

  const closeMenu = () => {
    removeClassList(sidebar, fadeInClass);
    changeDisplayStyle(sidebar, 'none');
    changeDisplayStyle(hamburguerMenu, 'block');
    changeDisplayStyle(closeMenuIcon, 'none');
  }

  hamburguerMenu.addEventListener('click', showMenu);
  closeMenuIcon.addEventListener('click', closeMenu);
})();
