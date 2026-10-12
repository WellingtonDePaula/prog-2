const formCadastro = document.getElementById("form-cadastro");

if (formCadastro) {
    formCadastro.addEventListener("submit", cadastrarAnimal);
}

async function cadastrarAnimal(e) {
    e.preventDefault();

    const nome = document.getElementById("campo-nome").value.trim();
    const raca = document.getElementById("campo-raca").value;
    const peso = document.getElementById("campo-peso").value;
    const sexo = document.getElementById("campo-sexo").value;

    const mensagem_erro = document.getElementById("mensagem-erro");
    mensagem_erro.textContent = "";
    
    let valido = true;
    let mensagens_temp = "";
    if(!nome) {
        valido = false;
        mensagens_temp += "O nome é obrigatório;\n";
    }
    if(!raca) {
        valido = false;
        mensagens_temp += "A raca é obrigatória;\n";
    }
    if(peso !== "" && Number(peso) < 0) {
        valido = false;
        mensagens_temp += "Valor mínimo: 0;\n";
    }
    if (!/^[FM]$/i.test(sexo.trim())) {
        valido = false;
        mensagens_temp += "Informe F ou M;\n";
    }
    if(!valido) {
        mensagem_erro.textContent = "Os seguintes campos estão com problema:\n" + mensagens_temp;
        return;
    }
    const msg = document.getElementById("mensagem");
    msg.textContent = "";

    const body = {
        "nome": nome,
        "raca": raca,
        "peso": Number(peso),
        "sexo": sexo.trim().toUpperCase()
    }

    try {
        const url = "http://127.0.0.1:5000/api/animais"
        const res = await fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body)
        });
        const data = await res.json();

        if (res.ok) {
            msg.textContent = `Animal ${data.nome} cadastrado com sucesso`
            formCadastro.reset();
        } else {
            msg.textContent = data.message || "Erro ao cadastrar.";
        }
    } catch(error) {
        msg.textContent = "Erro de conexão";
    }
}