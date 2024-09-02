let clicks = 0;
let btn = document.getElementById("btn");
let btn1 = document.getElementById("btn1");
let count = document.getElementById("count");
let text = document.getElementById("text_of_task");
let error = document.getElementById("text_of_error");
btn.onclick = popka;
btn1.onclick = popka1;
function popka() {
    clicks --;
    count.innerHTML = clicks;
    if (clicks === -18544) {
        text.innerHTML = 'CTF{Web_I5_n0T_H4RD_:)}'
    } else {
        text.innerHTML = 'Кажется счётчик уменьшается';
    };
};
function popka1() {
    clicks ++;
    if (clicks >= 10) {
        if (clicks >= 20) {
            if (clicks >= 100) {
                if (clicks >= 1000) {
                    if (clicks >= 10000) {
                        if (clicks > 20000) {
                            clicks = 0
                            error.innerHTML = 'Сайт не обрабатывает числа больше чем 20 000'
                        } else if (clicks === 20000) {
                            text.innerHTML = 'Ну мы же не спроста создали кнопку с айдишкой "btn", а может что-то наводящее есть в коде страницы?<br>Мы любим числа -8/25 or -8/18'
                        } else {
                            text.innerHTML = 'Ну ладно вы докликались до финала, надеюсь не вручную...<br>Cчётчик должен быть равен 20 000'
                        }
                    } else {
                        text.innerHTML = 'Ну вы уже должны были привыкнуть, счётчик должен быть равен 10 000'
                    }
                } else {
                    text.innerHTML = 'Ну это уже была последняя ошибка, счётчик должен быть равен 1 000'
                }
            } else {
                text.innerHTML = 'Опять ошибка, мы пытаемся всё пофиксить (Честно)<br>Cчётчик должен быть равен 100'
            }
        } else {
            text.innerHTML = 'Ой у нас произошла ошибка счётчик должен быть равен 20'
        }
    } else {
        text.innerHTML = 'Счётчик должен быть равен 10'
    };
    count.innerHTML = clicks;
};
function nUmBer_t0_gEt_f1ag() {
    text.innerHTML = '-18544'
} 