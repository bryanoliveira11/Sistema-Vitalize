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

class ProductMagnifierGlass {
  constructor() {
    this.productImage = document.querySelector('#product-image img');
    this.zoom = 2;
  }
  init() {
    if (!this.productImage) return;
    this.createMagnifier();
  }
  getCursorPosition(event) {
    const rect = this.productImage.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    return { x, y };
  }
  moveMagnifier = (event) => {
    event.preventDefault();
    const pos = this.getCursorPosition(event);
    const { width, height } = this.productImage;
    const magnifier = document.querySelector('#product-magnifier-glass');

    let x = pos.x;
    let y = pos.y;

    const magnifierWidth = magnifier.offsetWidth / this.zoom;
    const magnifierHeight = magnifier.offsetHeight / this.zoom;

    if (x > width - magnifierWidth) x = width - magnifierWidth;
    if (x < magnifierWidth) x = magnifierWidth;
    if (y > height - magnifierHeight) y = height - magnifierHeight;
    if (y < magnifierHeight) y = magnifierHeight;

    magnifier.style.left = `${x - magnifierWidth}px`;
    magnifier.style.top = `${y - magnifierHeight}px`;
    magnifier.style.backgroundPosition = `-${x * this.zoom - magnifierWidth}px -${y * this.zoom - magnifierHeight}px`;
  };
  createMagnifier() {
    const magnifier = document.createElement('div');
    magnifier.setAttribute('id', 'product-magnifier-glass');
    magnifier.setAttribute('class', 'shadow');
    this.productImage.parentElement.insertBefore(magnifier, this.productImage);

    magnifier.style.backgroundImage = `url('${this.productImage.src}')`;
    magnifier.style.backgroundRepeat = 'no-repeat';
    magnifier.style.backgroundSize = `${this.productImage.width * this.zoom}px ${this.productImage.height * this.zoom}px`;

    magnifier.style.position = 'absolute';
    magnifier.style.pointerEvents = 'none';

    this.productImage.addEventListener('mousemove', this.moveMagnifier);
    magnifier.addEventListener('mousemove', this.moveMagnifier);
  }
}

class NavBar {
  constructor() {
    this.navbarToggle = document.querySelector('.navbar-toggler');
  }
  init() {
    if (!this.navbarToggle) return;
    this.navbarToggle.addEventListener('click', () => this.handleToggle());
  }
  handleToggle() {
    const navBar = document.getElementById('ftco-nav');
    if (!navBar) return;
    if (navBar.classList.contains('is-toggled')) {
      removeClassList(navBar, 'is-toggled');
      changeDisplayStyle(navBar, 'none');
      return;
    }
    changeDisplayStyle(navBar, 'block');
    addClassList(navBar, 'is-toggled');
  }
}

class PreventPaste {
  constructor() {
    this.fields = document.querySelectorAll('.prevent-paste');
  }
  init() {
    if (this.fields.length === 0) return;
    this.preventPaste();
  }
  preventPaste() {
    for (const field of this.fields) {
      field.addEventListener('paste', (e) => {
        e.preventDefault();
      });
    }
  }
}

class UserSchedulesSearch {
  constructor() {
    this.schedulesField = document.getElementById('id_schedule');
  }
  init() {
    if (!this.schedulesField) return;
    this.createSearchBar();
    this.search();
  }
  createSearchBar() {
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.id = 'scheduleSearch';
    searchInput.className = 'form-control mb-2';
    searchInput.placeholder = 'Busque um E-mail ou ID...';
    this.schedulesField.parentNode.insertBefore(
      searchInput,
      this.schedulesField,
    );
  }
  search() {
    document
      .getElementById('scheduleSearch')
      .addEventListener('input', function () {
        let filter = this.value.toLowerCase();
        let options = document.querySelectorAll('#id_schedule option');

        options.forEach((option) => {
          let text = option.textContent.toLowerCase();
          if (text.includes(filter)) {
            option.style.display = '';
          } else {
            option.style.display = 'none';
          }
        });
      });
  }
}

// class SalesProductSearch {
//   constructor() {
//     this.productField = document.getElementById('id_products');
//   }
//   init() {
//     if (!this.productField) return;
//     this.createSearchBar();
//     this.search();
//   }
//   createSearchBar() {
//     const searchInput = document.createElement('input');
//     searchInput.type = 'text';
//     searchInput.id = 'productSearch';
//     searchInput.className = 'form-control mb-2';
//     searchInput.placeholder = 'Buscar Produtos...';
//     this.productField.parentNode.insertBefore(searchInput, this.productField);
//   }
//   search() {
//     document
//       .getElementById('productSearch')
//       .addEventListener('input', function () {
//         let filter = this.value.toLowerCase();
//         let options = document.querySelectorAll('#id_products option');

//         options.forEach((option) => {
//           let text = option.textContent.toLowerCase();
//           if (text.includes(filter)) {
//             option.style.display = '';
//           } else {
//             option.style.display = 'none';
//           }
//         });
//       });
//   }
// }

// class SelectInputCheckIcon {
//   constructor(field) {
//     this.selectField = field;
//   }
//   init() {
//     if (!this.selectField) return;
//     this.addCheckIcon();
//   }
//   addCheckIcon() {
//     const selectLabel = this.selectField.querySelector('label');
//     const labelText = selectLabel.innerText;
//     this.selectField.addEventListener('change', () => {
//       const icon = '<i class="fa-solid fa-circle-check"></i>';
//       let selectCount = 0;
//       this.selectField.querySelectorAll('option').forEach((option) => {
//         if (!option.selected) {
//           option.innerHTML = option.text;
//           return;
//         }
//         option.innerHTML = `${icon} ${option.text}`;
//         selectCount++;
//       });
//       selectLabel.innerHTML = `${labelText} &#8594; ${selectCount} ${icon}`;
//     });
//   }
// }

class CashoutUpdatePrices {
  constructor() {
    this.cashoutSelect = document.getElementById('id_cash_out');
    this.totalPriceElement = document.getElementById('total-price');
    this.subtotalElement = document.getElementById('subtotal');
    this.cashRegisterCashElement = document.getElementById('cashregister-cash');
  }
  init() {
    if (!this.totalPriceElement) return;
    this.updateTotalPrice();
    this.calculateTotalPrice();
  }
  calculateTotalPrice() {
    let totalPrice = 0;

    if (this.cashoutSelect) {
      const cashOutValue = parseFloat(this.cashoutSelect.value);
      totalPrice += isNaN(cashOutValue) ? 0 : cashOutValue;
    }

    this.totalPriceElement.textContent = 'R$ ' + totalPrice.toFixed(2);
    this.updateSubtotal(totalPrice);
  }
  updateSubtotal(totalPrice) {
    if (!this.cashRegisterCashElement) return;

    const cashRegisterCash = parseFloat(
      this.cashRegisterCashElement.textContent
        .replace('R$ ', '')
        .replace(',', '.'),
    );

    const subtotal = cashRegisterCash - totalPrice;
    this.subtotalElement.textContent = 'R$ ' + subtotal.toFixed(2);
  }
  updateTotalPrice() {
    if (this.cashoutSelect) {
      this.cashoutSelect.addEventListener(
        'input',
        this.calculateTotalPrice.bind(this),
      );
    }
  }
}

class DigitalClock {
  constructor() {
    this.clock = document.getElementById('clock');
  }
  init() {
    if (!this.clock) return;
    setInterval(() => this.updateClock(), 1000);
    this.updateClock();
  }
  updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    this.clock.textContent = `${hours}:${minutes}:${seconds}`;
  }
}

class HandleSalesProducts {
  constructor() {
    this.selectedProducts = document.getElementById('id_products');
    this.productsTable = document.getElementById('products-table-body');
  }
  init() {
    if (!this.selectedProducts) return;
    this.handleSelectedProducts();
    this.handleUnselectedProducts();
    this.handleClearProducts();
    this.handleQuantityChange();
  }
  handleSelectedProducts() {
    $(this.selectedProducts).on('select2:select', (e) => {
      const data = e.params.data;
      this.createRow(data);
    });
  }
  handleUnselectedProducts() {
    $(this.selectedProducts).on('select2:unselect', (e) => {
      const data = e.params.data;
      if (data.disabled === false) {
        this.removeRow(data.id);
      }
    });
  }
  handleClearProducts() {
    $(this.selectedProducts).on('select2:clear', () => {
      this.clearAllRows();
    });
  }
  createRow(data) {
    const newRow = `
      <tr id="product-${data.id}" data-unit-price="${data.price}">
        <td><b></b></td>
        <td>${data.text}</td>
        <td><input type="number" class="quantity-input"
        name="quantities[${data.id}]" value="1" min="1"></td>
        <td class="product-price">R$ ${parseFloat(data.price).toFixed(2)}</td>
      </tr>`;
    $(this.productsTable).append(newRow);
  }
  removeRow(productId) {
    $(`#product-${productId}`).remove();
  }
  clearAllRows() {
    $(this.productsTable).empty();
  }
  handleQuantityChange() {
    $(this.productsTable).on('input', '.quantity-input', (e) => {
      const quantityInput = $(e.target);
      const row = quantityInput.closest('tr');
      const unitPrice = parseFloat(row.data('unit-price'));
      const newQuantity = parseInt(quantityInput.val(), 10);

      if (newQuantity > 0) {
        const updatedPrice = unitPrice * newQuantity;
        row.find('.product-price').text(`R$ ${updatedPrice.toFixed(2)}`);
      }
    });
  }
}

new DismissFlashMessages().init();
new HandlePasswordTipsStyles().init();
new HandlePhoneNumberMask().init();
new ShowHidePassword().init();
new LogoutLinks().init();
new BackToTopButton().init();
new ProductMagnifierGlass().init();
new NavBar().init();
new PreventPaste().init();
new UserSchedulesSearch().init();
new CashoutUpdatePrices().init();
new DigitalClock().init();
new HandleSalesProducts().init();
