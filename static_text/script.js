document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('textInput');
    const totalChars = document.getElementById('totalChars');
    const letters = document.getElementById('letters');
    const upperCase = document.getElementById('upperCase');
    const lowerCase = document.getElementById('lowerCase');
    const spaces = document.getElementById('spaces');
    const specialChars = document.getElementById('specialChars');
    const digits = document.getElementById('digits');
    const words = document.getElementById('words');

    function analyzeText(text) {
        const stats = {
            totalChars: text.length,
            letters: 0,
            upperCase: 0,
            lowerCase: 0,
            spaces: 0,
            specialChars: 0,
            digits: 0,
            words: text.trim() === '' ? 0 : text.trim().split(/\s+/).length
        };

        for (const char of text) {
            if (/[a-zA-Zа-яА-ЯёЁ]/.test(char)) {
                stats.letters++;
                if (char === char.toUpperCase()) {
                    stats.upperCase++;
                }
                if (char === char.toLowerCase()) {
                    stats.lowerCase++;
                }
            } else if (/\s/.test(char)) {
                stats.spaces++;
            } else if (/\d/.test(char)) {
                stats.digits++;
            } else if (char !== '') {
                stats.specialChars++;
            }
        }

        return stats;
    }

    function updateStats(stats) {
        totalChars.textContent = stats.totalChars;
        letters.textContent = stats.letters;
        upperCase.textContent = stats.upperCase;
        lowerCase.textContent = stats.lowerCase;
        spaces.textContent = stats.spaces;
        specialChars.textContent = stats.specialChars;
        digits.textContent = stats.digits;
        words.textContent = stats.words;
    }

    textInput.addEventListener('input', (e) => {
        const text = e.target.value;
        const stats = analyzeText(text);
        updateStats(stats);
    });
}); 