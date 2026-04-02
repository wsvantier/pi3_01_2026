async function carregarEstoque() {
    try {
        const response = await fetch("/api/estoque");
        const dados = await response.json();

        const tbody = document.getElementById("tabela-estoque");
        tbody.innerHTML = "";

        dados.forEach(item => {
            const linha = `
                <tr>
                    <td>${item.nome}</td>
                    <td>${item.unidade_medida}</td>
                    <td>${item.estoque_total}</td>
                </tr>
            `;
            tbody.innerHTML += linha;
        });

    } catch (erro) {
        console.error("Erro ao carregar estoque:", erro);
    }
}

// Executa ao carregar a página
carregarEstoque();
