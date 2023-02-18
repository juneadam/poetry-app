

// const popoverLinks = document.querySelectorAll('.line-text');
// const tooltips = document.querySelector('.hover-info');

// // Pass the button, the tooltip, and some options, and Popper will do the
// // magic positioning for you:

// for (int(i)=0; i < popoverLinks.length(); i++) {
// Popper.createPopper(popoverLinks[i], tooltips[i], {
//   placement: 'right',
// });

// }

// function show() {
//     for (const tooltip of tooltips) {
//     tooltip.setAttribute('data-show', '');
  
//     // We need to tell Popper to update the tooltip position
//     // after we show the tooltip, otherwise it will be incorrect
//     popperInstance.update();
//     }
//   }
  
//   function hide() {
//     for (const tooltip of tooltips) {
//     tooltip.removeAttribute('data-show');
//     }
//   }
  
  const showEvents = ['mouseenter', 'focus'];
  const hideEvents = ['mouseleave', 'blur'];
  
  showEvents.forEach((event) => {
    for (const popoverLink of popoverLinks) {
    popoverLink.addEventListener(event, show);
    }
  });
  
  hideEvents.forEach((event) => {
    for (const popoverLink of popoverLinks) {
    popoverLink.addEventListener(event, hide);
    }
  });