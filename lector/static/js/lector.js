document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("barcode-input");
    const list = document.getElementById("series-list");

    input.focus();

    input.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            e.preventDefault();
            const serie = input.value.trim();
            if (serie.length === 0) return;
            sendSerie(serie);
            input.value = "";
        }
    });

    function sendSerie(serie) {
        fetch("/admin/inventario/ordencompra/add-serie/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify({ orden_id: ordenId, nro_serie: serie })
        }).then(res => {
            if (res.ok) {
                const li = document.createElement("li");
                li.textContent = serie;
                list.appendChild(li);
            }
        })
        .catch((e) => {
            console.error("Error al enviar la serie.", e);
        });
    }

    function getCookie(name) {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith(name + '='));
        return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
    }
});
