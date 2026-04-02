async function carregarConsumo() {
    try {
        const response = await fetch("/api/consumo");
        const dados = await response.json();

        const tbody = document.getElementById("tabela-consumo");
        tbody.innerHTML = "";

        if (dados.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5'>Nenhum consumo registrado</td></tr>";
            return;
        }

        dados.forEach(item => {
            const linha = `
                <tr>
                    <td>${item.produto}</td>
                    <td>${item.quantidade}</td>
                    <td>${item.data}</td>
                    <td>${item.refeicao || '-'}</td>
                    <td>${item.responsavel || '-'}</td>
                </tr>
            `;
            tbody.innerHTML += linha;
        });

    } catch (erro) {
        console.error("Erro ao carregar consumo:", erro);
    }
}

carregarConsumo();