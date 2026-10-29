let tempoEspera;

async function autocompletar () {
  clearTimeout(tempoEspera);
  const termo = document.getElementById("busca").value.trim();
  const lista = document.getElementById("sugestoes");
  const erro = document.getElementById("erro-busca");
  erro.textContent = "";

  if (termo.length < 3) {
    lista.classList.add("hidden");
    lista.innerHTML = "";
    if (termo.length > 0) {
      erro.textContent = "Digite ao menos 3 letras";
    }
    return;
  }
  console.log("Digitando");
  tempoEspera = setTimeout(async () => {
    const res = await fetch(`/api/items?search=${encodeURIComponent(termo)}`);
    const itens = await res.json();
    console.log("Executei a busca no servidor!");

    lista.innerHTML = "";
    if (itens.length === 0) {
      lista.classList.add("hidden");
      return;
    }

    itens.forEach(item => {
      const li = document.createElement("li");
      li.textContent = item.nome;
      li.className = "px-3 py-2 cursor-pointer hover:bg-blue-50 text-gray-700 text-sm";
      li.onclick = () => carregarItem(item.id, item.nome);
      lista.appendChild(li);
    });
    lista.classList.remove("hidden");
  }, 500);
}

/* Autocomplete  */
document.getElementById("busca").addEventListener("input", autocompletar);

/* Carregar dados do item */
async function carregarItem(id, nome) {
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


/*  Deletar (DELETE) */
document.getElementById("btn-deletar").addEventListener("click", async (e) => {
  e.preventDefault();
  if (!confirm("Tem certeza que deseja excluir este item?")) return;

  const id = document.getElementById("item_id").value;
  const msg = document.getElementById("mensagem");

  const res = await fetch(`/api/items/${id}`, { method: "DELETE" });
  const data = await res.json();

  if (res.ok) {
    msg.className = "mt-4 p-3 rounded-lg text-sm bg-green-100 text-green-800";
    msg.textContent = data.mensagem;
    document.getElementById("formulario-edicao").classList.add("hidden");
    document.getElementById("busca").value = "";
  } else {
    msg.className = "mt-4 p-3 rounded-lg text-sm bg-red-100 text-red-800";
    msg.textContent = data.erro || "Erro ao deletar.";
  }
});

document.getElementById("form-edicao").addEventListener("submit", atualizarItem);

async function atualizarItem(e) {
  e.preventDefault();

  const msg = document.getElementById("mensagem");
  msg.textContent = "";

  if (!validarEdicao()) return;

  const quantidade = document.getElementById("quantidade").value;
  const valor = document.getElementById("valor").value;

  const body = {
    id: Number(document.getElementById("item_id").value),
    nome: document.getElementById("nome").value.trim(),
    quantidade: quantidade === "" ? 0 : Number(quantidade),
    valor: valor === "" ? 0.0 : Number(valor)
  };

  try {
    const res = await fetch("/api/atualizar_item", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    const data = await res.json();

    if (res.ok) {
      msg.className = "mt-4 p-3 rounded-lg text-sm bg-green-100 text-green-800";
      msg.textContent = "Item atualizado com sucesso.";
      document.getElementById("busca").value = data.nome;
    } else {
      msg.className = "mt-4 p-3 rounded-lg text-sm bg-red-100 text-red-800";
      msg.textContent = data.message || "Erro ao atualizar.";
    }
  } catch (err) {
    msg.className = "mt-4 p-3 rounded-lg text-sm bg-red-100 text-red-800";
    msg.textContent = "Erro de conexão ao atualizar o item.";
  }
}