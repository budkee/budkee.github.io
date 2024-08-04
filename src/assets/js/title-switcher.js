// title-switcher.js

// Array com os títulos em diferentes idiomas
const titles = [
    "Ooie!",
    "Hi, there!",
    "¡Hola! ¿Que tal?"
  ];
  
// Índice inicial
let currentIndex = 0;

// Função para alterar o título com animação
function changeTitle() {
// Obtenha o elemento span
const titleElement = document.getElementById("dynamic-title");

// Adicione a animação de deslizar para fora
titleElement.style.animation = "slide-out 2s forwards"; // Duração de 2 segundos

// Depois que a animação de deslizar para fora terminar, altere o texto e deslize para dentro
setTimeout(() => {
    // Atualize o texto do span
    titleElement.textContent = titles[currentIndex];

    // Atualize o índice para o próximo título
    currentIndex = (currentIndex + 1) % titles.length;

    // Adicione a animação de deslizar para dentro
    titleElement.style.animation = "slide-in 2s forwards"; // Duração de 2 segundos
}, 2000); // Tempo deve ser igual à duração da animação de slide-out
}

// Função para inicializar o título sem animação
function initializeTitle() {
    const titleElement = document.getElementById("dynamic-title");
    titleElement.textContent = titles[currentIndex];
    currentIndex = (currentIndex + 1) % titles.length;
}

// Inicializa o título ao carregar a página pela primeira vez
document.addEventListener("DOMContentLoaded", () => {
    initializeTitle();

    // Inicia a troca de título após o primeiro intervalo completo
    setTimeout(() => {
        setInterval(changeTitle, 5000);
    }, 3000); // Tempo inicial antes da primeira mudança
});
