const closeButton = document.querySelector('.loopple-alert.loopple-alert-dismissible .close');

if (closeButton) {
    closeButton.onclick = function() {
        const alertElement = document.querySelector('.loopple-alert');

        if (alertElement) {
            alertElement.classList.add('loopple-opacity-0');

            setTimeout(function() {
                alertElement.remove();
            }, 1000);
        }
    };
}
