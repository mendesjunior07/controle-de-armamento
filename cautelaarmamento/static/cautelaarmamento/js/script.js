const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function() {
    document.querySelector("#sidebar").classList.toggle("expand");
});


function updateSubcategoriasArmamento(rowId) {
    var formRow = document.getElementById(rowId);
    var categoriaId = formRow.querySelector(".categoria-select-armamento").value;

    var subcategoriaSelect = formRow.querySelector(".subcategoria-select-armamento");
    subcategoriaSelect.innerHTML = '<option value="">Selecione uma Subcategoria</option>';

    if (categoriaId) {
        fetch(`/subcategorias_armamento/${categoriaId}/`)
            .then((response) => response.json())
            .then((data) => {
                data.forEach((subcategoria) => {
                    var option = document.createElement("option");
                    option.value = subcategoria.id;
                    option.textContent = subcategoria.nome;
                    subcategoriaSelect.appendChild(option);
                });

                $(subcategoriaSelect).select2({
                    placeholder: 'Digite para buscar...',
                    allowClear: true
                });
            })
            .catch(error => console.error('Erro ao buscar subcategorias de armamento:', error));
    }
}

function updateSubcategoriasMunicao(rowId) {
    var formRow = document.getElementById(rowId);
    var categoriaId = formRow.querySelector(".categoria-select-municao").value;

    var subcategoriaSelect = formRow.querySelector(".subcategoria-select-municao");
    subcategoriaSelect.innerHTML = '<option value="">Selecione uma Subcategoria</option>';

    if (categoriaId) {
        fetch(`/subcategorias_municao/${categoriaId}/`)
            .then((response) => response.json())
            .then((data) => {
                data.forEach((subcategoria) => {
                    var option = document.createElement("option");
                    option.value = subcategoria.id;
                    option.textContent = subcategoria.nome;
                    subcategoriaSelect.appendChild(option);
                });

                // Initialize or reinitialize the Select2 plugin for the updated select element
                $(subcategoriaSelect).select2({
                    placeholder: 'Digite para buscar...',
                    allowClear: true
                });
            })
            .catch(error => console.error('Erro ao buscar subcategorias de munição:', error));
    }
}