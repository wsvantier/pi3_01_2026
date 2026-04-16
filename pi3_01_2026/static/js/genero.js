async function carregarGeneros() {
    try {
        const response = await fetch("/api/genero");
        const dados = await response.json();

        const tbody = document.getElementById("tabela-genero");

        let html = "";

        dados.forEach(g => {
            let classe = "";

            // Verifica se está abaixo do mínimo
            if (g.estoque_total < g.estoque_minimo) {
                classe = "linha-baixa";
            }

            html += `
                <tr class="${classe}">
                    <td>${g.nome}</td>
                    <td>${g.unidade_medida}</td>
                    <td>
                        ${g.estoque_minimo}
                        <br>
                        <small>Atual: ${g.estoque_total}</small>
                    </td>
                </tr>
            `;
        });

        tbody.innerHTML = html;

    } catch (erro) {
        console.error("Erro ao carregar dados:", erro);
    }
}

// Carrega ao abrir a página
document.addEventListener("DOMContentLoaded", carregarGeneros);