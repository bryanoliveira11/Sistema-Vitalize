const changeDisplayStyle = (element, display) => {
  if (element) element.style.display = display;
};

const addClassList = (element, value) => {
  if (element) element.classList.add(value);
};

const removeClassList = (element, value) => {
  if (element) element.classList.remove(value);
};

function ChangeDisplayAnimationEnd(element) {
  element.addEventListener(
    'animationend',
    () => {
      changeDisplayStyle(element, 'none');
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
          addClassList(parentElement, 'hide-message');
          ChangeDisplayAnimationEnd(parentElement);
        }
      });
    }
  }
}

class HandlePasswordTipsStyles {
  constructor() {
    this.passwordField = document.querySelector('#id_password');
    this.helpTexts = Array.from(
      document.querySelectorAll('.helptext-p.password'),
    );
  }

  init() {
    if (!this.passwordField || !this.helpTexts) return;
    this.passwordField.addEventListener('keyup', () => this.handleStyle());
  }

  handleStyle() {
    const conditions = [
      !(this.passwordField.value.length < 8),
      /^(?=.*[A-Z])/.test(this.passwordField.value),
      /^(?=.*[a-z])/.test(this.passwordField.value),
      /^(?=.*\d)/.test(this.passwordField.value),
    ];
    const errorColor = '#dc3545';
    const successColor = '#28a745';

    conditions.forEach((condition, index) => {
      const color = condition ? successColor : errorColor;
      this.changeHelpTextColor(index, color);

      if (!condition) {
        this.addIcon(index, 'fa-circle-exclamation', errorColor);
        this.removeIcon(index, 'fa-check');
      } else {
        this.addIcon(index, 'fa-check', successColor);
        this.removeIcon(index, 'fa-circle-exclamation');
      }
    });
  }

  changeHelpTextColor(index, color) {
    if (!this.helpTexts[index]) return;
    this.helpTexts[index].style.color = color;
  }

  addIcon(index, iconClass, color) {
    if (!this.helpTexts[index]) return;

    let icon = this.helpTexts[index].querySelector(`.${iconClass}`);
    if (!icon) {
      icon = document.createElement('i');
      icon.className = `fa-solid ${iconClass}`;
      icon.style.marginLeft = '8px';
      icon.style.color = color;
      this.helpTexts[index].appendChild(icon);
    }
  }

  removeIcon(index, iconClass) {
    if (!this.helpTexts[index]) return;
    const icon = this.helpTexts[index].querySelector(`.${iconClass}`);
    if (icon) {
      this.helpTexts[index].removeChild(icon);
    }
  }
}

class HandlePhoneNumberMask {
  constructor() {
    this.phoneNumber = document.querySelector('#id_phone_number');
  }
  init() {
    if (!this.phoneNumber) return;
    this.phoneNumber.addEventListener('input', (e) => this.handlePhone(e));
  }
  handlePhone(event) {
    let input = event.target;
    input.value = this.phoneMask(input.value);
  }
  phoneMask(value) {
    if (!value) return '';
    value = value.replace(/\D/g, '');
    value = value.replace(/(\d{2})(\d)/, '($1) $2');
    value = value.replace(/(\d)(\d{4})$/, '$1-$2');
    return value;
  }
}

class ShowHidePassword {
  constructor() {
    this.passwordField = document.querySelector('#id_password');
    if (!this.passwordField) return;
    this.inputGroup = this.passwordField.parentElement;
    if (!this.inputGroup) return;
    this.eyeIconContainer = this.inputGroup.querySelector('.input-group-text');
    this.eyeIcon = this.inputGroup.querySelector('.input-group-text .fa-eye');
  }
  init() {
    if (!this.inputGroup || !this.eyeIconContainer || !this.eyeIcon) return;
    this.updateInputType();
  }
  updateInputType() {
    let is_password_visible = false;
    this.eyeIconContainer.addEventListener('click', () => {
      if (is_password_visible) {
        this.passwordField.type = 'password';
        removeClassList(this.eyeIcon, 'fa-eye-slash');
        addClassList(this.eyeIcon, 'fa-eye');
      } else {
        this.passwordField.type = 'text';
        removeClassList(this.eyeIcon, 'fa-eye');
        addClassList(this.eyeIcon, 'fa-eye-slash');
      }
      is_password_visible = !is_password_visible;
    });
  }
}

class LogoutLinks {
  constructor() {
    this.linksLogout = Array.from(
      document.querySelectorAll('.user-logout-link'),
    );
    this.formLogout = document.querySelector('.form-logout');
  }
  init() {
    for (const link of this.linksLogout) {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        this.formLogout.submit();
      });
    }
  }
}

class BackToTopButton {
  constructor() {
    this.backToTopBtn = document.getElementById('btn-back-to-top');
  }
  init() {
    if (!this.backToTopBtn) return;
    this.backToTopBtn.addEventListener('click', () => this.backToTop());
    window.onscroll = () => this.scroll();
  }
  scroll() {
    if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
    ) {
      changeDisplayStyle(this.backToTopBtn, 'block');
    } else {
      changeDisplayStyle(this.backToTopBtn, 'none');
    }
  }
  backToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }
}

new DismissFlashMessages().init();
new HandlePasswordTipsStyles().init();
new HandlePhoneNumberMask().init();
new ShowHidePassword().init();
new LogoutLinks().init();
new BackToTopButton().init();
