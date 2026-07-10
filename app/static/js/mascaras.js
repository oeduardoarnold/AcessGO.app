/**
 * mascaras.js
 * Funções de máscara/formatação para campos de formulário (CPF, telefone,
 * número de cartão de crédito, validade e CVV) usadas nas telas de reserva.
 *
 * Como usar: basta adicionar a classe correspondente ao <input>:
 *   class="mask-cpf"       -> 000.000.000-00
 *   class="mask-telefone"  -> (00) 00000-0000
 *   class="mask-cartao"    -> 0000 0000 0000 0000
 *   class="mask-validade"  -> MM/AA
 *   class="mask-cvv"       -> apenas números, até 4 dígitos
 */

document.addEventListener('DOMContentLoaded', function () {

    // Mantém apenas dígitos em uma string
    function apenasNumeros(valor) {
        return (valor || '').replace(/\D/g, '');
    }

    // ---------- CPF: 000.000.000-00 ----------
    function formatarCPF(valor) {
        let v = apenasNumeros(valor).slice(0, 11);
        v = v.replace(/(\d{3})(\d)/, '$1.$2');
        v = v.replace(/(\d{3})(\d)/, '$1.$2');
        v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
        return v;
    }

    // ---------- Telefone: (00) 00000-0000 ou (00) 0000-0000 ----------
    function formatarTelefone(valor) {
        let v = apenasNumeros(valor).slice(0, 11);
        if (v.length > 10) {
            // Celular: (00) 00000-0000
            v = v.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
        } else if (v.length > 5) {
            // Fixo: (00) 0000-0000
            v = v.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
        } else if (v.length > 2) {
            v = v.replace(/^(\d{2})(\d{0,5}).*/, '($1) $2');
        } else if (v.length > 0) {
            v = v.replace(/^(\d{0,2}).*/, '($1');
        }
        return v;
    }

    // ---------- Cartão de crédito: 0000 0000 0000 0000 ----------
    function formatarCartao(valor) {
        let v = apenasNumeros(valor).slice(0, 19); // suporta cartões com até 19 dígitos
        v = v.replace(/(\d{4})(?=\d)/g, '$1 ');
        return v.trim();
    }

    // ---------- Validade do cartão: MM/AA ----------
    function formatarValidade(valor) {
        let v = apenasNumeros(valor).slice(0, 4);
        if (v.length >= 3) {
            v = v.replace(/^(\d{2})(\d{0,2}).*/, '$1/$2');
        }
        return v;
    }

    // ---------- CVV: apenas números ----------
    function formatarCVV(valor) {
        return apenasNumeros(valor).slice(0, 4);
    }

    function aplicarMascara(seletor, formatador) {
        document.querySelectorAll(seletor).forEach(function (input) {
            input.addEventListener('input', function () {
                const posicaoCursor = input.selectionStart;
                const tamanhoAntes = input.value.length;
                input.value = formatador(input.value);
                const diferenca = input.value.length - tamanhoAntes;
                // Reposiciona o cursor de forma aproximada após a formatação
                if (posicaoCursor !== null) {
                    const novaPosicao = Math.max(0, posicaoCursor + diferenca);
                    input.setSelectionRange(novaPosicao, novaPosicao);
                }
            });
        });
    }

    aplicarMascara('.mask-cpf', formatarCPF);
    aplicarMascara('.mask-telefone', formatarTelefone);
    aplicarMascara('.mask-cartao', formatarCartao);
    aplicarMascara('.mask-validade', formatarValidade);
    aplicarMascara('.mask-cvv', formatarCVV);
});
