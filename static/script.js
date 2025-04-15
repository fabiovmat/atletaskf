function abrirModal(id) {
  fetch(`/api/atleta/${id}`)
    .then(response => response.json())
    .then(data => {
      document.getElementById("loader").style.display = "block";
      document.getElementById("modalNome").innerText = data.nome;
      document.getElementById("modalIdade").innerText = data.idade;
      document.getElementById("modalTreino").innerText = data.tempo_treino;
      document.getElementById("modalEditar").href = `/cadastro?editar=${data.id}`;
      document.getElementById("modalDeletar").action = `/deletar/${data.id}`;

      const container = document.getElementById("modalCategorias");
      container.innerHTML = "";

      for (let i = 1; i <= 5; i++) {
        const categoria = data[`categoria${i}`];
        const nota = data[`nota${i}`];
        const classificacao = data[`classificacao${i}`];

        if (categoria) {
          const div = document.createElement("div");
          div.className = "categoria-info";
          div.innerHTML = `
            <p><strong>${categoria}</strong></p>
            <p>Nota: ${nota !== null ? parseFloat(nota).toFixed(2) : '0.00'} | Classificação: ${classificacao || "N/A"}</p>
          `;
          container.appendChild(div);
        }
      }
      document.getElementById("loader").style.display = "none";

      document.getElementById("modal").style.display = "block";
    })
    .catch(err => {
      console.error("Erro ao buscar atleta:", err);
      alert("Erro ao carregar informações do atleta.");
    });
}

function fecharModal(event) {
  if (
    event.target.id === "modal" ||
    event.target.classList.contains("fechar")
  ) {
    document.getElementById("modal").style.display = "none";
  }
}
