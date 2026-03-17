// ===== TEST NAVIGATION =====

function getSlide(index) {
    return document.getElementById(`q-slide-${index}`);
}

function isAnswered(questionIndex) {
    const radios = document.querySelectorAll(`input[name="q${questionIndex}"]`);
    return Array.from(radios).some(r => r.checked);
}

function updateProgress(current, total) {
    const pct = ((current - 1) / total) * 100;
    const bar = document.getElementById('progressBar');
    const text = document.getElementById('progressText');
    if (bar) bar.style.width = pct + '%';
    if (text) text.textContent = `Frage ${current} / ${total}`;
}

function nextQuestion(current, total) {
    if (!isAnswered(current)) {
        shakeSlide(current);
        return;
    }
    const currentSlide = getSlide(current);
    const nextSlide = getSlide(current + 1);
    if (!nextSlide) return;

    currentSlide.classList.remove('active');
    nextSlide.classList.add('active');
    updateProgress(current + 1, total);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function prevQuestion(current) {
    const currentSlide = getSlide(current);
    const prevSlide = getSlide(current - 1);
    if (!prevSlide) return;

    currentSlide.classList.remove('active');
    prevSlide.classList.add('active');
    updateProgress(current - 1, typeof totalQuestions !== 'undefined' ? totalQuestions : 8);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function shakeSlide(index) {
    const slide = getSlide(index);
    if (!slide) return;
    slide.style.animation = 'none';
    slide.offsetHeight; // reflow
    slide.style.animation = 'shake 0.4s ease';

    const hint = slide.querySelector('.no-answer-hint');
    if (!hint) {
        const msg = document.createElement('p');
        msg.className = 'no-answer-hint';
        msg.textContent = 'Bitte wähle eine Antwort aus.';
        msg.style.cssText = 'color:#F87171;font-size:0.85rem;margin-top:-1.5rem;margin-bottom:1rem;text-align:center;';
        const nav = slide.querySelector('.question-nav');
        if (nav) slide.insertBefore(msg, nav);
        setTimeout(() => msg.remove(), 3000);
    }
}

// Auto-advance on selection
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('testForm');
    if (!form) return;

    form.querySelectorAll('input[type="radio"]').forEach(radio => {
        radio.addEventListener('change', () => {
            const name = radio.name; // e.g. "q3"
            const qIndex = parseInt(name.replace('q', ''));
            const total = typeof totalQuestions !== 'undefined' ? totalQuestions : 8;

            // Remove existing hint if any
            const slide = getSlide(qIndex);
            const hint = slide ? slide.querySelector('.no-answer-hint') : null;
            if (hint) hint.remove();

            // Auto-advance after short delay (not on last question)
            if (qIndex < total) {
                setTimeout(() => nextQuestion(qIndex, total), 320);
            }
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        const activeSlide = document.querySelector('.question-slide.active');
        if (!activeSlide) return;
        const current = parseInt(activeSlide.dataset.index);
        const total = typeof totalQuestions !== 'undefined' ? totalQuestions : 8;

        if (e.key === 'ArrowRight' || e.key === 'Enter') {
            if (current < total) nextQuestion(current, total);
        }
        if (e.key === 'ArrowLeft') {
            if (current > 1) prevQuestion(current);
        }
    });
});

// ===== RESULT ANIMATIONS =====
document.addEventListener('DOMContentLoaded', () => {
    // Animate score bars
    const bars = document.querySelectorAll('.score-bar-fill');
    if (bars.length > 0) {
        setTimeout(() => {
            bars.forEach(bar => {
                const targetWidth = bar.dataset.width + '%';
                bar.style.width = targetWidth;
            });
        }, 300);
    }
});

// ===== SHAKE KEYFRAME (injected via JS) =====
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-6px); }
        40% { transform: translateX(6px); }
        60% { transform: translateX(-4px); }
        80% { transform: translateX(4px); }
    }
`;
document.head.appendChild(style);
