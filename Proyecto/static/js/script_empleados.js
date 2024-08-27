async function loadempleados() {
    try {
        const response = await fetch('/api/empleados', {  // Use lowercase 'empleados'
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('sin respuesta de la red');
        }

        const data = await response.json();
        console.log('datos recibidos:', data);

        if (!data.Empleados || !data.Empleados.length) {
            console.error('No data found or empty array returned');
            return;
        }

        const empTbody = document.getElementById('empleados-tbody');
        if (!empTbody) {
            console.error('Elemento ID no encontrado');
            return;
        }

        empTbody.innerHTML = '';

        data.Empleados.forEach(empleado => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${empleado.id}</td>
                <td>${empleado.apellido_nombre}</td>
                <td>${empleado.direccion}</td>
                <td>${empleado.telefono}</td>
                <td>${empleado.dias}</td>
                <td>${empleado.horarios}</td>
            `;
            empTbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error de carga:', error);
    }
}

window.onload = function() {
    loadempleados();
};



async function manageempleados(action) {
    const formData = new FormData();

    if (action === "add_modify") {
        formData.append("action", "add_modify");
        formData.append("id", document.getElementById("id").value);
        formData.append("apellido_nombre", document.getElementById("apellido_nombre").value);
        formData.append("direccion", document.getElementById("direccion").value);
        formData.append("telefono", document.getElementById("telefono").value);
        formData.append("dias", document.getElementById("dias").value);
        formData.append("horarios", document.getElementById("horarios").value);
    } else if (action === "delete") {
        formData.append("action", "delete");
        formData.append("id", document.querySelector("#deleteForm input[name='id']").value);
    }

    try {
        const response = await fetch('/empleados', {  // Use lowercase 'empleados'
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error de carga');
        }

        const result = await response.json();
        console.log('Server response:', result);

        // Reload the employees after operation
        loadempleados();
    } catch (error) {
        console.error('Error en el manejo de empleado:', error);
    }
}


