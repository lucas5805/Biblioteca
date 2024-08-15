async function loadRentas() {
    try {
        const response = await fetch('/api/rentas', {
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('sin respuesta de la red');
        }

        const data = await response.json();
        console.log('Data received:', data);

        if (!data.Rentas || !data.Rentas.length) {
            console.error('No data found or empty array returned');
            return;
        }

        const renTbody = document.getElementById('rentas-tbody');
        if (!renTbody) {
            console.error('Error de carga');
            return;
        }

        renTbody.innerHTML = '';

        data.Rentas.forEach(Renta => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${Renta.id}</td>
                <td>${Renta.fechainicio}</td>
                <td>${Renta.fechadevolucion}</td>
                <td>${Renta.id_cliente}</td>
                <td>${Renta.id_libro}</td>
            `;
            renTbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error de carga:', error);
    }
}

window.onload = function() {
    loadRentas();
};

async function manageRentas(action) {
    const formData = new FormData();

    if (action === "add_modify") {
        formData.append("action", "add_modify");
        formData.append("id", document.getElementById("id").value);
        formData.append("fechainicio", document.getElementById("fechainicio").value);
        formData.append("fechadevolucion", document.getElementById("fechadevolucion").value);
        formData.append("id_cliente", document.getElementById("id_cliente").value);
        formData.append("id_libro", document.getElementById("id_libro").value);
    } else if (action === "delete") {
        formData.append("action", "delete");
        formData.append("id", document.querySelector("#deleteForm input[name='id']").value);
    }

    try {
        const response = await fetch('/Rentas', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error de carga');
        }

        const result = await response.json();
        console.log('Server response:', result);

        // Optionally reset forms after successful action
        if (action === "add_modify" || action === "delete") {
            document.getElementById("RentasForm").reset();
            document.getElementById("deleteForm").reset();
        }

        loadRentas();
    } catch (error) {
        console.error('Error en el manejo de rentas:', error);
    }
}

