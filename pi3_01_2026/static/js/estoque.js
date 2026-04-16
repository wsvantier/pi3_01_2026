// =============================
// Função: calcular dias restantes
// =============================
function calcularDias(validadeStr) {
    const hoje = new Date();
    const validade = new Date(validadeStr);

    // Evita erro de timezone
    hoje.setHours(0, 0, 0, 0);
    validade.setHours(0, 0, 0, 0);

    const diffMs = validade - hoje;
    return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}


// =============================
// Carregar estoque geral
// =============================
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


// =============================
// Carregar lotes (com lógica completa)
// =============================
async function carregarLote() {
    try {
        const response = await fetch("/api/lote");
        const dados = await response.json();

        const tbody = document.getElementById("tabela-lote");

        // =============================
        // ORDENAÇÃO (vencidos no topo)
        // =============================
        dados.sort((a, b) => {
            const diasA = calcularDias(a.validade);
            const diasB = calcularDias(b.validade);

            const vencidoA = a.vencido || diasA < 0;
            const vencidoB = b.vencido || diasB < 0;

            // 1. Vencidos primeiro
            if (vencidoA && !vencidoB) return -1;
            if (!vencidoA && vencidoB) return 1;

            // 2. Ambos vencidos → mais atrasado primeiro
            if (vencidoA && vencidoB) return diasA - diasB;

            // 3. Não vencidos → menor prazo primeiro
            return diasA - diasB;
        });

        let html = "";

        dados.forEach(item => {
            let classe = "";
            let status = "";

            const dias = calcularDias(item.validade);

            // =============================
            // DEFINIÇÃO DE STATUS
            // =============================
            if (item.vencido || dias < 0) {
                classe = "linha-vencida";
                status = `🔴 Vencido há ${Math.abs(dias)} dias`;
            } 
            else if (dias <= 90) {
                classe = "linha-alerta";
                status = `🟡 Vence em ${dias} dias`;
            } 
            else {
                status = `✅ Em dia`;
            }

            html += `
                <tr class="${classe}">
                    <td>${item.produto}</td>
                    <td>
                        ${item.validade_formatada ?? item.validade}
                        <br>
                        <small>${status}</small>
                    </td>
                    <td>${item.quantidade_atual}</td>
                </tr>
            `;
        });

        tbody.innerHTML = html;

    } catch (erro) {
        console.error("Erro ao carregar lote:", erro);
    }
}


// =============================
// Inicialização
// =============================
document.addEventListener("DOMContentLoaded", () => {
    carregarEstoque();
    carregarLote();
});