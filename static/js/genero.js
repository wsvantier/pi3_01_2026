async function carregarGeneros() {
    try {
        const response = await fetch("/api/genero");
        const dados = await response.json();

        const tbody = document.getElementById("tabela-genero");
        tbody.innerHTML = "";

        dados.forEach(g => {
            const linha = `
                <tr>
                    <td>${g.nome}</td>
                    <td>${g.unidade_medida}</td>
                    <td>${g.estoque_minimo}</td>
                </tr>
            `;
            tbody.innerHTML += linha;
        });

    } catch (erro) {
        console.error("Erro ao carregar dados:", erro);
    }
}

// Carrega ao abrir a página
carregarGeneros();