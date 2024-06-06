const changeDisplayStyle = (element, display) => {
  if (element) element.style.display = display;
}

const addClassList = (element, value) => {
  if (element) element.classList.add(value);
}

const removeClassList = (element, value) => {
  if (element) element.classList.remove(value);
}
