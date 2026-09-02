const selectProduto = document.getElementById("selectProduto");
const inputQuantidade = document.getElementById("inputQuantidade");
const btnAdicionar = document.getElementById("btnAdicionar");
const tabelaCarrinho = document.querySelector("#tabelaCarrinho tbody");
const spanTotal = document.getElementById("spanTotal");
const hiddenInputs = document.getElementById("hiddenInputs");
const formCompra = document.getElementById("formCompra");

let carrinho = {};

btnAdicionar.addEventListener("click", function() {
    const opcao = selectProduto.options[selectProduto.selectedIndex];
    if (!opcao.value) {
        alert("Selecione um produto.");
        return;
    }
    
    const produtoId = opcao.value;
    const nome = opcao.getAttribute("data-nome");
    const preco = parseFloat(opcao.getAttribute("data-preco"));
    const estoque = parseInt(opcao.getAttribute("data-estoque"));
    const quantidade = parseInt(inputQuantidade.value);

    if (isNaN(quantidade) || quantidade <= 0) {
        alert("Informe uma quantidade válida.");
        return;
    }

    let quantidadeTotal = quantidade;
    if (carrinho[produtoId]) {
        quantidadeTotal += carrinho[produtoId].quantidade;
    }

    if (quantidadeTotal > estoque) {
        alert("Quantidade em estoque insuficiente para este produto.");
        return;
    }

    if (!carrinho[produtoId]) {
        carrinho[produtoId] = {
            nome: nome,
            preco: preco,
            quantidade: quantidade
        };
    } else {
        carrinho[produtoId].quantidade += quantidade;
    }

    renderizarCarrinho();
});

function renderizarCarrinho() {
    tabelaCarrinho.innerHTML = "";
    hiddenInputs.innerHTML = "";
    let totalGeral = 0;

    for (const [id, item] of Object.entries(carrinho)) {
        const subtotal = item.preco * item.quantidade;
        totalGeral += subtotal;

        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.nome}</td>
            <td>R$ ${item.preco.toFixed(2)}</td>
            <td>${item.quantidade}</td>
            <td>R$ ${subtotal.toFixed(2)}</td>
            <td><button type="button" onclick="removerItem('${id}')" class="btn-remover">Remover</button></td>
        `;
        tabelaCarrinho.appendChild(tr);

        hiddenInputs.innerHTML += `
            <input type="hidden" name="produto_id[]" value="${id}">
            <input type="hidden" name="quantidade[]" value="${item.quantidade}">
        `;
    }

    spanTotal.textContent = totalGeral.toFixed(2);
}

let removerItem = function(id) {
    delete carrinho[id];
    renderizarCarrinho();
};

formCompra.addEventListener("submit", function(e) {
    if (Object.keys(carrinho).length === 0) {
        e.preventDefault();
        alert("O carrinho está vazio. Adicione produtos antes de finalizar a compra.");
    }
});

