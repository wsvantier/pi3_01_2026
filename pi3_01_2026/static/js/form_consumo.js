async function carregarProdutos() {
    const response = await fetch('/api/genero');
    const data = await response.json();

    const select = document.getElementById('produto_id');

    // Opção padrão obrigatória
    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.textContent = "-- Selecione um produto --";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    select.appendChild(defaultOption);

    data.forEach(p => {
        const option = document.createElement('option');
        option.value = p.id;
        option.textContent = p.nome;
        select.appendChild(option);
    });
}

async function carregarLotes(produto_id) {
    const response = await fetch(`/api/lotes/${produto_id}`);
    const data = await response.json();

    const select = document.getElementById('lote_id');
    select.innerHTML = '<option value="">-- Selecione o lote --</option>';

    data.forEach(lote => {
        const option = document.createElement('option');
        option.value = lote.id;
        option.textContent = `Val: ${lote.validade} | Qtd: ${lote.quantidade}`;
        select.appendChild(option);
    });
}

// Espera o DOM carregar
window.addEventListener('DOMContentLoaded', () => {
    carregarProdutos();

    document.getElementById('produto_id').addEventListener('change', function () {
        carregarLotes(this.value);
    });
});