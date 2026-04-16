async function carregarEstoque() {
    try {
        const response = await fetch("/api/estoque");
        const dados = await response.json();

        const tbody = document.getElementById("tabela-estoque");

        let html = "";

        dados.forEach(item => {
            html += `
                <tr>
                    <td>${item.nome}</td>
                    <td>${item.unidade_medida}</td>
                    <td>${item.estoque_total}</td>
                </tr>
            `;
        });

        tbody.innerHTML = html;

    } catch (erro) {
        console.error("Erro ao carregar estoque:", erro);
    }
}


async function carregarLote() {
    try {
        const response = await fetch("/api/lote");
        const dados = await response.json();

        const tbody = document.getElementById("tabela-lote");

        let html = "";
        const hoje = new Date();

        dados.forEach(item => {
            let classe = "";

            // Data no formato ISO (YYYY-MM-DD)
            const validade = new Date(item.validade);

            // Diferença em meses (~)
            const diffMeses = (validade - hoje) / (1000 * 60 * 60 * 24 * 30);

            if (item.vencido) {
                classe = "linha-vencida";
            } else if (diffMeses <= 3) {
                classe = "linha-alerta";
            }

            html += `
                <tr class="${classe}">
                    <td>${item.produto}</td>
                    <td>${item.validade_formatada ?? item.validade}</td>
                    <td>${item.quantidade_atual}</td>
                </tr>
            `;
        });

        tbody.innerHTML = html;

    } catch (erro) {
        console.error("Erro ao carregar lote:", erro);
    }
}


// Executa ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    carregarEstoque();
    carregarLote();
});