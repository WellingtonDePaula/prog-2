let tempoEspera;


/* Carregar dados do item */
async function carregarItem(id, nome) {
  document.getElementById("form-busca").classList.add("hidden");
  document.getElementById("sugestoes").classList.add("hidden");
  document.getElementById("busca").value = nome;

  const res = await fetch(`/api/items/${id}`);
  if (!res.ok) return;
  const item = await res.json();

  document.getElementById("item_id").value    = item.id;
  document.getElementById("nome").value        = item.nome;
  document.getElementById("quantidade").value  = item.quantidade;
  document.getElementById("valor").value       = item.valor;
  document.getElementById("formulario-edicao").classList.remove("hidden");
  document.getElementById("mensagem").className = "mt-4 p-3 rounded-lg text-sm hidden";
}

/*  Validação client-side */
function validarEdicao() {
  let valido = true;
  ["nome", "quantidade", "valor"].forEach(c => {
    document.getElementById("erro-" + c).textContent = "";
  });

  const nome = document.getElementById("nome").value.trim();
  const qtd = document.getElementById("quantidade").value;
  const val = document.getElementById("valor").value;

  if (!nome) {
    document.getElementById("erro-nome").textContent = "O nome é obrigatório.";
    valido = false;
  }
  if (qtd !== "" && Number(qtd) < 0) {
    document.getElementById("erro-quantidade").textContent = "Valor mínimo: 0";
    valido = false;
  }
  if (val !== "" && Number(val) < 0) {
    document.getElementById("erro-valor").textContent = "Valor mínimo: 0";
    valido = false;
  }
  return valido;
}

async function deletar_item(e) {
  e.preventDefault();

  const id = document.getElementById("item_id").value;
  const formEdicao = document.getElementById("formulario-edicao");
  const formBusca = document.getElementById("form-busca");

  const mensagem = document.getElementById("mensagem");
  const url = "/api/items/" + id;
  console.log(url);
  try {
    const res = await fetch(url, {
      method: "DELETE",
      headers: {"Content-Type": "application/json"}
    });

    if(res.ok) {
      formEdicao.classList.add("hidden");
      document.getElementById("busca").value = "";
      formBusca.classList.remove("hidden");
    } else {
      throw new Error("Erro ao deletar item: " + res.status);
    }
  } catch(error) {
    mensagem.innerHTML = "Erro ao deletar item";
  }
}

// Busca por letras
async function busca_item(e) {
  const value = busca.value;

  const url = "/api/items?search="+encodeURIComponent(value);

  const erro = document.getElementById("erro-busca");
  erro.innerText = "";

  try {
    const res = await fetch(url, {
      method: "GET",
      headers: {"Content-Type": "application/json"}
    });

    const sugestoes = document.getElementById("sugestoes");
    sugestoes.innerHTML = "";
    if(res.ok) {
      const dados = await res.json();



      if(dados.length > 0) {
        sugestoes.classList.remove("hidden");
      } else {
        sugestoes.classList.add("hidden");
      }

      dados.forEach(dado => {
        const li = document.createElement("li");
        li.textContent = dado.nome;
        li.className = "px-3 py-2 cursor-pointer hover:bg-gray-100";
        li.addEventListener("click", () => carregarItem(dado.id, dado.nome));
        sugestoes.appendChild(li);
      });

    } else {
      throw new Error("Erro na busca: " + res.status);
    }
  } catch (error) {
    erro.innerText = "Erro na busca";
  }
}

/* Atualizar (PUT) */
async function atualizar_item (e) {
  e.preventDefault();
  if (!validarEdicao()) return;

  const id = document.getElementById("item_id").value;
  const msg = document.getElementById("mensagem");
  const quantidade = document.getElementById("quantidade").value;
  const valor = document.getElementById("valor").value;

  const res = await fetch(`/api/items/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      nome: document.getElementById("nome").value.trim(),
      quantidade: quantidade === "" ? 0 : Number(quantidade),
      valor: valor === "" ? 0.0 : Number(valor)
    })
  });
  const data = await res.json();

  if (res.ok) {
    msg.className = "mt-4 p-3 rounded-lg text-sm bg-green-100 text-green-800";
    msg.textContent = "Item atualizado com sucesso!";
  } else {
    msg.className = "mt-4 p-3 rounded-lg text-sm bg-red-100 text-red-800";
    msg.textContent = data.erro || "Erro ao atualizar.";
  }
}
const busca = document.getElementById("busca");
busca.addEventListener("input", busca_item);

document.getElementById("btn-deletar").addEventListener("click", deletar_item)
document.getElementById("btn-atualizar").addEventListener("click", atualizar_item);

