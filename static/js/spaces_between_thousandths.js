
    const formatContent = (element) => {
        const text = element.textContent.replace(/\s/g, ''); // убираем пробелы
        const number = parseFloat(text);

        if (!Number.isNaN(number) && !element.dataset.formatted) { // проверяем, не было ли уже отформатировано
            const formatted = number.toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
            element.textContent = formatted;
            element.dataset.formatted = true; // устанавливаем флаг, что элемент был отформатирован
        }
    };

    const mutationObserver = new MutationObserver(
        (mutations) => mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => { // обрабатываем только добавленные узлы
                if (node.nodeType === Node.TEXT_NODE && node.parentNode.tagName === 'TH') { // проверяем, что узел - текст внутри элемента <th>
                    formatContent(node.parentNode); // форматируем содержимое элемента <th>
                }
            });
        })
    );

    document.querySelectorAll('.table').forEach((element) => {
        element.querySelectorAll('th').forEach((th) => {
            formatContent(th); // форматируем уже существующие элементы <th>
            mutationObserver.observe(th, { characterData: true }); // наблюдаем за изменениями текста внутри элементов <th>
        });
    });
