const changeDisplayStyle = (element, display) => {
  if (element) element.style.display = display;
}

const addClassList = (element, value) => {
  if (element) element.classList.add(value);
}

const removeClassList = (element, value) => {
  if (element) element.classList.remove(value);
}

function ChangeDisplayAnimationEnd(element) {
  element.addEventListener(
    'animationend',
    () => {
      element.style.display = 'none';
    },
    { once: true },
  );
}

class DismissFlashMessages {
  constructor() {
    this.dismissMessageBtns = Array.from(
      document.querySelectorAll('.dismiss-flash-message'),
    );
  }
  init() {
    if (!this.dismissMessageBtns) return;
    for (const btn of this.dismissMessageBtns) {
      btn.addEventListener('click', () => {
        const parentElement = btn.parentElement;
        if (parentElement.classList.contains('message')) {
          parentElement.classList.add('hide-message');
          ChangeDisplayAnimationEnd(parentElement);
        }
      });
    }
  }
}

new DismissFlashMessages().init();