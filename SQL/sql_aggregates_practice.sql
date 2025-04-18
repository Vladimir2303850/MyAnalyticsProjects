-- Задание 1: Уникальные значения количества книг
SELECT DISTINCT amount FROM book;

-- Задание 2: Статистика по авторам (книги и экземпляры)
SELECT 
    author AS "Автор",
    COUNT(title) AS "Различных_книг",
    SUM(amount) AS "Количество_экземпляров"
FROM book
GROUP BY author;

-- Задание 3: Минимальная, максимальная и средняя цена по авторам
SELECT 
    author,
    MIN(price) AS "Минимальная цена",
    MAX(price) AS "Максимальная цена",
    AVG(price) AS "Средняя цена"
FROM book
GROUP BY author;

-- Задание 4: Расчет стоимости с НДС и без
SELECT 
    author,
    ROUND(SUM(price * amount), 2) AS "Стоимость",
    ROUND(SUM(price * amount) * 0.18 / 1.18, 2) AS "НДС",
    ROUND(SUM(price * amount) / 1.18, 2) AS "Стоимость_без_НДС"
FROM book
GROUP BY author;

-- Задание 5: Общая статистика цен
SELECT 
    MIN(price) AS "Минимальная цена",
    MAX(price) AS "Максимальная цена",
    ROUND(AVG(price), 2) AS "Средняя цена"
FROM book;

-- Задание 6: Средняя цена и стоимость для книг 5-14 экз.
SELECT 
    ROUND(AVG(price), 2) AS "Средняя цена",
    ROUND(SUM(price * amount), 2) AS "Стоимость"
FROM book
WHERE amount BETWEEN 5 AND 14;

-- Задание 7: Стоимость книг авторов (исключая определённые книги)
SELECT 
    author,
    ROUND(SUM(price * amount), 2) AS "Стоимость"
FROM book
WHERE title NOT IN ('Идиот', 'Белая гвардия')
GROUP BY author
HAVING SUM(price * amount) > 5000
ORDER BY "Стоимость" DESC;
