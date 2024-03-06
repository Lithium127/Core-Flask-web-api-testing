
const current_endpoint = window.location.href;

export function fetchHTMLFromForm(form, response_target) {
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        fetch(url_endpoint, {
            method: "POST",
            body: new FormData(form)
        })
        .then(response => response.text())
        .then(html => {
            response_target.innerHTML = html;
        })
        .catch(error => console.error("Error: ", error));
        
    });
};