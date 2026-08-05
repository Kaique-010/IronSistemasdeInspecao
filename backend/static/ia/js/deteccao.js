(function () {

    var form = document.getElementById("form-deteccao");
    var btn = document.getElementById("btn-detectar");
    var area = document.getElementById("area-resultado");
    var campoExemplo = document.getElementById("campo-exemplo");
    var listaExemplos = document.getElementById("lista-exemplos");
    var inputImagem = document.getElementById("id-imagem");
    var esteira = document.getElementById("esteira");
    var legendaEsteira = esteira
        ? esteira.querySelector(".iron-esteira-legenda")
        : null;

    function limparSelecaoExemplo() {
        var selecionados = listaExemplos.querySelectorAll(".selecionado");
        for (var i = 0; i < selecionados.length; i++) {
            selecionados[i].classList.remove("selecionado");
        }
    }

    if (listaExemplos) {
        listaExemplos.addEventListener("click", function (evento) {
            var alvo = evento.target.closest(".iron-exemplo");
            if (!alvo) return;

            limparSelecaoExemplo();
            alvo.classList.add("selecionado");
            campoExemplo.value = alvo.getAttribute("data-arquivo");
            inputImagem.value = "";
        });
    }

    if (inputImagem) {
        inputImagem.addEventListener("change", function () {
            if (inputImagem.value) {
                limparSelecaoExemplo();
                campoExemplo.value = "";
            }
        });
    }

    function estadoCarregando(ativar) {
        btn.disabled = ativar;
        if (ativar) {
            btn.innerHTML = '<span class="iron-spinner"></span> Analisando...';
        } else {
            btn.innerHTML = "Executar detecção";
        }
    }

    function mostrarMensagem(tipo, texto) {
        area.innerHTML =
            '<div class="iron-status iron-status-' +
            tipo +
            '">' +
            texto +
            "</div>";
    }

    function montarListaDetecoes(detecoes) {
        if (!detecoes.length) {
            return "<p class='iron-subtitulo'>Nenhum objeto detectado nesta imagem.</p>";
        }

        var itens = detecoes
            .map(function (d) {
                var pct = Math.round(d.confianca * 100);
                return (
                    "<li><span class='iron-nome'>" +
                    d.nome +
                    "</span><span class='iron-conf'>" +
                    pct +
                    "%</span></li>"
                );
            })
            .join("");

        return "<ul class='iron-lista-deteccoes'>" + itens + "</ul>";
    }

    form.addEventListener("submit", function (evento) {
        evento.preventDefault();

        if (!campoExemplo.value && !inputImagem.files.length) {
            mostrarMensagem("erro", "Escolha um exemplo ou envie uma imagem.");
            return;
        }

        estadoCarregando(true);

        if (legendaEsteira) {
            legendaEsteira.textContent = "processando imagem...";
        }

        var dados = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: dados,
            headers: {
                "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value
            }
        })
            .then(function (resposta) {
                return resposta.json().then(function (corpo) {
                    return { ok: resposta.ok, corpo: corpo };
                });
            })
            .then(function (resultado) {
                estadoCarregando(false);

                if (legendaEsteira) {
                    legendaEsteira.textContent = "inspeção concluída";
                }

                var corpo = resultado.corpo;

                if (!resultado.ok || corpo.erro) {
                    mostrarMensagem("erro", corpo.erro || "Falha ao executar a detecção.");
                    return;
                }

                var tempo = corpo.tempo ? " em " + corpo.tempo + "s" : "";

                area.innerHTML =
                    "<div class='iron-resultado'><img src='" +
                    corpo.imagem +
                    "' alt='Resultado'></div>" +
                    "<div class='iron-status iron-status-ok'>" +
                    corpo.total +
                    " objeto(s) detectado(s) com " +
                    corpo.modelo_nome +
                    tempo +
                    "</div>" +
                    montarListaDetecoes(corpo.detecoes || []);
            })
            .catch(function () {
                estadoCarregando(false);
                if (legendaEsteira) {
                    legendaEsteira.textContent = "aguardando imagem";
                }
                mostrarMensagem(
                    "erro",
                    "Erro de comunicação com o servidor. Rode o backend na máquina host para habilitar a detecção."
                );
            });
    });
})();
