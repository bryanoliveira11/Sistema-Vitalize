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

class HandleCashRegisterPrices {
  constructor() {
    this.cashoutSelect = document.getElementById('id_cash_out');
    this.cashinSelect = document.getElementById('id_cash_in');
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

    if (this.cashinSelect) {
      const cashInValue = parseFloat(this.cashinSelect.value);
      totalPrice += isNaN(cashInValue) ? 0 : cashInValue;
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

    if (this.cashoutSelect) {
      const subtotal = cashRegisterCash - totalPrice;
      this.subtotalElement.textContent = 'R$ ' + subtotal.toFixed(2);
      return;
    }

    if (this.cashinSelect) {
      const subtotal = cashRegisterCash + totalPrice;
      this.subtotalElement.textContent = 'R$ ' + subtotal.toFixed(2);
    }
  }
  updateTotalPrice() {
    if (this.cashoutSelect) {
      this.cashoutSelect.addEventListener(
        'input',
        this.calculateTotalPrice.bind(this),
      );
      return;
    }
    if (this.cashinSelect) {
      this.cashinSelect.addEventListener(
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

class HandleSalesForm {
  constructor() {
    this.schedulesField = document.getElementById('id_schedule');
    this.selectedProducts = document.getElementById('id_products');
    this.productsTable = document.getElementById('products-table-body');
    this.selectedServices = document.getElementById('id_services');
    this.servicesTable = document.getElementById('services-table-body');
    this.totalPriceElement = document.getElementById('total-price');
    this.productsPrice = 0;
    this.servicesPrice = 0;
  }

  init() {
    if (!this.selectedProducts || !this.totalPriceElement) return;
    this.loadFromLocalStorage();
    this.setupEventListeners();
    this.updateAllTotals();
  }

  loadFromLocalStorage() {
    try {
      const savedProducts =
        JSON.parse(localStorage.getItem('selectedProducts')) || [];
      const savedServices =
        JSON.parse(localStorage.getItem('selectedServices')) || [];

      savedProducts.forEach((product) => this.addProductToDOM(product));
      savedServices.forEach((service) => this.addServiceToDOM(service));

      this.updateAllTotals();
    } catch (error) {
      console.error('Error loading data from local storage');
    }
  }

  saveToLocalStorage() {
    const selectedProducts = this.getTableData(this.productsTable, true);
    const selectedServices = this.getTableData(this.servicesTable, false);

    localStorage.setItem('selectedProducts', JSON.stringify(selectedProducts));
    localStorage.setItem('selectedServices', JSON.stringify(selectedServices));
  }

  setupEventListeners() {
    if (this.schedulesField) {
      $(this.schedulesField).on('select2:select', (e) =>
        this.handleScheduleSelect(e),
      );
      $(this.schedulesField).on('select2:unselect', () => this.clearServices());
    }

    $(this.selectedProducts).on('select2:select', (e) =>
      this.handleProductSelect(e),
    );
    $(this.selectedProducts).on('select2:unselect', (e) =>
      this.handleProductUnselect(e),
    );
    $(this.selectedProducts).on('select2:clear', () => this.clearAllProducts());

    $(this.selectedServices).on('select2:select', (e) =>
      this.handleServiceSelect(e),
    );
    $(this.selectedServices).on('select2:unselect', (e) =>
      this.handleServiceUnselect(e),
    );
    $(this.selectedServices).on('select2:clear', () => this.clearAllServices());

    $(this.productsTable).on('input', '.quantity-input', (e) =>
      this.handleQuantityChange(e),
    );
  }

  handleScheduleSelect(e) {
    const scheduleData = e.params.data;
    this.clearServices();

    if (scheduleData.services) {
      scheduleData.services.forEach((service) => {
        this.addServiceToDOM(service);
        this.addSelectOption(this.selectedServices, service);
      });
    }

    this.updateAllTotals();
    this.saveToLocalStorage();
  }

  handleProductSelect(e) {
    this.addProductToDOM(e.params.data);
    this.updateAllTotals();
    this.saveToLocalStorage();
  }

  handleProductUnselect(e) {
    if (e.params.data.disabled === false) {
      this.removeItemFromDOM(this.productsTable, e.params.data.id);
      this.updateAllTotals();
      this.saveToLocalStorage();
    }
  }

  handleServiceSelect(e) {
    this.addServiceToDOM(e.params.data);
    this.updateAllTotals();
    this.saveToLocalStorage();
  }

  handleServiceUnselect(e) {
    if (e.params.data.disabled === false) {
      this.removeItemFromDOM(this.servicesTable, e.params.data.id);
      this.updateAllTotals();
      this.saveToLocalStorage();
    }
  }

  handleQuantityChange(e) {
    const quantityInput = e.target;
    const row = quantityInput.closest('tr');
    const unitPrice = parseFloat(row.dataset.unitPrice);
    const newQuantity = parseInt(quantityInput.value, 10) || 1;

    row.querySelector('.product-price').textContent =
      `R$ ${(unitPrice * newQuantity).toFixed(2)}`;
    this.updateAllTotals();
    this.saveToLocalStorage();
  }

  updateAllTotals() {
    this.productsPrice = this.calculateTotal(this.productsTable);
    this.servicesPrice = this.calculateTotal(this.servicesTable);
    const totalPrice = this.productsPrice + this.servicesPrice;
    this.totalPriceElement.textContent = `R$ ${totalPrice.toFixed(2)}`;
  }

  calculateTotal(table) {
    let total = 0;
    Array.from(table.querySelectorAll('tr')).forEach((row) => {
      const unitPrice = parseFloat(row.dataset.unitPrice);
      const quantity = parseInt(
        row.querySelector('.quantity-input')?.value || '1',
        10,
      );
      total += unitPrice * quantity;
    });
    return total;
  }

  addProductToDOM(product) {
    if (document.getElementById(`product-${product.id}`)) return;

    const quantity = product.quantity || 1;
    const totalPrice = parseFloat(product.price) * quantity;

    const newRow = document.createElement('tr');
    newRow.id = `product-${product.id}`;
    newRow.dataset.unitPrice = product.price;
    newRow.dataset.slug = product.slug;
    newRow.innerHTML = `
      <input type="hidden" value="${product.text}" class="table-text">
      <td class="table-image">
        <a href="/product/${product.slug}" target="_blank">
          <img src="${product.image}" alt="Product Image">
        </a>
      </td>
      <td>${product.text_no_price}</td>
      <td>R$ ${parseFloat(product.price).toFixed(2)}</td>
      <td id="product-quantity"><input type="number" class="quantity-input"
      name="quantities[${product.id}]" value="${quantity}" min="1"></td>
      <td class="product-price">R$ ${totalPrice.toFixed(2)}</td>
    `;
    this.productsTable.appendChild(newRow);
    this.addSelectOption(this.selectedProducts, product);
  }

  addServiceToDOM(service) {
    if (document.getElementById(`service-${service.id}`)) return;

    const newRow = document.createElement('tr');
    newRow.id = `service-${service.id}`;
    newRow.dataset.unitPrice = service.price;
    newRow.innerHTML = `
      <input type="hidden" value="${service.text}" class="table-text">
      <td class="table-image"><img src="${service.image}" alt="Service Image"></td>
      <td>${service.text_no_price}</td>
      <td class="service-description">${service.description || ''}</td>
      <td class="service-price">R$ ${parseFloat(service.price).toFixed(2)}</td>
    `;
    this.servicesTable.appendChild(newRow);
    this.addSelectOption(this.selectedServices, service);
  }

  removeItemFromDOM(table, itemId) {
    const row = table.querySelector(
      `#${table.id.includes('product') ? 'product' : 'service'}-${itemId}`,
    );
    if (row) row.remove();
  }

  clearAllProducts() {
    this.productsTable.innerHTML = '';
    this.updateAllTotals();
    this.saveToLocalStorage();
  }

  clearAllServices() {
    this.servicesTable.innerHTML = '';
    this.updateAllTotals();
    this.saveToLocalStorage();
  }

  clearServices() {
    this.clearAllServices();
    $(this.selectedServices).empty().trigger('change');
  }

  getTableData(table, hasQuantity) {
    return Array.from(table.querySelectorAll('tr')).map((row) => {
      return {
        id: row.id.split('-')[1],
        image: row.querySelector('.table-image img').src,
        text: row.querySelector('.table-text').value,
        text_no_price: row.cells[1].textContent,
        price: parseFloat(row.dataset.unitPrice),
        ...(hasQuantity && {
          quantity:
            parseInt(row.querySelector('.quantity-input').value, 10) || 1,
        }),
        ...(row.cells[2].classList.contains('service-description') && {
          description: row.cells[2].textContent,
        }),
      };
    });
  }

  addSelectOption(selectElement, item) {
    if (!$(selectElement).find(`option[value="${item.id}"]`).length) {
      const option = new Option(item.text, item.id, true, true);
      $(selectElement).append(option).trigger('change');
    }
  }
}

document.addEventListener('DOMContentLoaded', function () {
  if (window.location.pathname === '/cashregister/') {
    localStorage.clear();
  }
});

new DismissFlashMessages().init();
new HandlePasswordTipsStyles().init();
new HandlePhoneNumberMask().init();
new ShowHidePassword().init();
new LogoutLinks().init();
new BackToTopButton().init();
new ProductMagnifierGlass().init();
new NavBar().init();
new PreventPaste().init();
new HandleCashRegisterPrices().init();
new DigitalClock().init();
new HandleSalesForm().init();
