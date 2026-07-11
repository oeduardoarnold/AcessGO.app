/**
 * carrossel.js
 * Faz as setas de qualquer ".carrossel-wrapper" rolarem sua ".carrossel-track"
 * horizontalmente. Usado nas seções "Hotéis", "Pontos Turísticos" e
 * "Experiências" da home (index.html).
 */

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.carrossel-wrapper').forEach(function (wrapper) {
        var track = wrapper.querySelector('.carrossel-track');
        var btnPrev = wrapper.querySelector('.carrossel-prev');
        var btnNext = wrapper.querySelector('.carrossel-next');

        if (!track || !btnPrev || !btnNext) {
            return;
        }

        function quantidadeDeScroll() {
            // Rola aproximadamente 80% da largura visível a cada clique
            return track.clientWidth * 0.8;
        }

        btnPrev.addEventListener('click', function () {
            track.scrollBy({ left: -quantidadeDeScroll(), behavior: 'smooth' });
        });

        btnNext.addEventListener('click', function () {
            track.scrollBy({ left: quantidadeDeScroll(), behavior: 'smooth' });
        });
    });
});
