async function loadMiembros() {
    try {
        const response = await fetch('/api/Miembros', {
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('sin respuesta de la red');
        }

        const data = await response.json();
        console.log('Data received:', data);

        if (!data.Miembros || !data.Miembros.length) {
            console.error('Sin datos o tabla vacia');
            return;
        }

        const MiemTbody = document.getElementById('Miembros-tbody');
        if (!MiemTbody) {
            console.error('Error de carga');
            return;
        }

        MiemTbody.innerHTML = '';

        data.Miembros.forEach(Miembro => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${Miembro.id}</td>
                <td>${Miembro.apellido_nombre}</td>
                <td>${Miembro.direccion}</td>
                <td>${Miembro.telefono}</td>
            `;
            MiemTbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error de carga:', error);
    }
}

window.onload = function() {
    loadMiembros();
};


async function manageMiembros(action) {
    const formData = new FormData();

    if (action === "add_modify") {
        formData.append("action", "add_modify");
        formData.append("id", document.getElementById("id").value);
        formData.append("apellido_nombre", document.getElementById("apellido_nombre").value);
        formData.append("direccion", document.getElementById("direccion").value);  // Ensure the ID matches
        formData.append("telefono", document.getElementById("telefono").value);
    } else if (action === "delete") {
        formData.append("action", "delete");
        formData.append("id", document.querySelector("#deleteForm input[name='id']").value);
    }

    try {
        const response = await fetch('/Miembros', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error de carga');
        }

        const result = await response.json();
        console.log('Server response:', result);

        // Reload the employees after operation
        loadMiembros();
    } catch (error) {
        console.error('Error en el manejo de miembros:', error);
    }
}