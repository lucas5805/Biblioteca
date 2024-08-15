async function loadLibros() {
    try {
        const response = await fetch('/api/libros', {
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Sin respuesta de la red');
        }

        const data = await response.json();
        console.log('datos recividos:', data);

        if (!data.libros || !data.libros.length) {
            console.error('Sin libros o tabla vacia');
            return;
        }

        const librosTbody = document.getElementById('libros-tbody');
        librosTbody.innerHTML = '';

        data.libros.forEach(libro => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${libro.id}</td>
                <td>${libro.nombre}</td>
                <td>${libro.disponibilidad ? "Sí" : "No"}</td>
            `;
            librosTbody.appendChild(tr);
        });
    } catch (error) {
        console.error('Error de carga:', error);
    }
}

window.onload = function() {
    loadLibros();
};




async function manageLibro(action) {
    const formData = new FormData();

    if (action === "add_modify") {
        formData.append("action", "add_modify");
        formData.append("id", document.getElementById("id").value);
        formData.append("nombre", document.getElementById("nombre").value);
        formData.append("disponibilidad", document.getElementById("disponibilidad").checked);
    } else if (action === "delete") {
        formData.append("action", "delete");
        formData.append("id", document.querySelector("#deleteForm input[name='id']").value);
    }

    try {
        const response = await fetch('/libros', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('sin respuesta de la red');
        }

        const result = await response.json();
        console.log('Server response:', result);

        // Reload the libros after operation
        loadLibros();
    } catch (error) {
        console.error('Error en el manejo de libros:', error);
    }
}
