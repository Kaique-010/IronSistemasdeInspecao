(function () {

    function csrfToken() {
        var cookie = document.cookie.split(";").map(function (c) {
            return c.trim();
        });
        for (var i = 0; i < cookie.length; i++) {
            if (cookie[i].indexOf("csrftoken=") === 0) {
                return cookie[i].slice("csrftoken=".length);
            }
        }
        return "";
    }

    function adicionarSwitcher(empresas, atual) {
        var nav = document.querySelector(".app-header .navbar-nav.ms-auto");
        if (!nav || !empresas.length) return;

        var li = document.createElement("li");
        li.className = "nav-item dropdown d-none d-sm-inline-block";
        li.style.marginRight = "0.5rem";

        var atualNome = "Empresa";
        for (var i = 0; i < empresas.length; i++) {
            if (empresas[i].slug === atual) {
                atualNome = empresas[i].nome;
                break;
            }
        }

        var rotulo = document.createElement("a");
        rotulo.className = "nav-link dropdown-toggle";
        rotulo.href = "#";
        rotulo.setAttribute("data-bs-toggle", "dropdown");
        rotulo.setAttribute("role", "button");
        rotulo.innerHTML =
            '<span class="iron-tenant-badge" style="margin:0">' +
            (atual ? "/" + atual + "/ " : "sem empresa ") +
            "</span> " +
            atualNome;

        var menu = document.createElement("div");
        menu.className = "dropdown-menu dropdown-menu-end";
        menu.innerHTML = '<span class="dropdown-header">Trocar de empresa</span><div class="dropdown-divider"></div>';

        empresas.forEach(function (empresa) {
            var item = document.createElement("button");
            item.type = "button";
            item.className = "dropdown-item";
            item.textContent = "/" + empresa.slug + "/  " + empresa.nome;
            if (empresa.slug === atual) {
                item.classList.add("active");
            }
            item.addEventListener("click", function () {
                var f = document.createElement("form");
                f.method = "POST";
                f.action = "/tenant/trocar/";
                f.style.display = "none";

                var token = document.createElement("input");
                token.type = "hidden";
                token.name = "csrfmiddlewaretoken";
                token.value = csrfToken();

                var campo = document.createElement("input");
                campo.type = "hidden";
                campo.name = "empresa";
                campo.value = empresa.slug;

                var destino = document.createElement("input");
                destino.type = "hidden";
                destino.name = "destino";
                destino.value = window.location.pathname;

                f.appendChild(token);
                f.appendChild(campo);
                f.appendChild(destino);
                document.body.appendChild(f);
                f.submit();
            });
            menu.appendChild(item);
        });

        li.appendChild(rotulo);
        li.appendChild(menu);
        nav.insertBefore(li, nav.firstChild);
    }

    fetch("/tenant/minhas/", { headers: { "Accept": "application/json" } })
        .then(function (resposta) {
            if (!resposta.ok) return null;
            return resposta.json();
        })
        .then(function (dados) {
            if (dados && dados.empresas) {
                adicionarSwitcher(dados.empresas, dados.atual);
            }
        })
        .catch(function () {});
})();
