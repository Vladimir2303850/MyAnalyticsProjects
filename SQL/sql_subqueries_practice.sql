-- Задание 1: Книги с ценой <= средней (сортировка по убыванию цены)
SELECT 
    author,
    title,
    price
FROM book
WHERE price <= (SELECT AVG(price) FROM book)
ORDER BY price DESC;

-- Задание 2: Книги с ценой в диапазоне min_price <= price <= min_price+150
SELECT 
    author,
    title,
    price
FROM book
WHERE price <= (SELECT MIN(price) FROM book) + 150
ORDER BY price ASC;

-- Задание 3: Книги с уникальным количеством экземпляров
SELECT 
    author,
    title,
    amount
FROM book
WHERE amount IN (
    SELECT amount 
    FROM book 
    GROUP BY amount 
    HAVING COUNT(*) = 1
);

-- Задание 4: Книги с ценой меньше максимальной из минимальных цен по авторам
SELECT 
    author,
    title,
    price
FROM book
WHERE price < (
    SELECT MAX(min_price) 
    FROM (
        SELECT MIN(price) AS min_price 
        FROM book 
        GROUP BY author
    ) AS author_min_prices
);

-- Задание 5: Расчет необходимого заказа книг
SELECT 
    title,
    author,
    amount,
    (SELECT MAX(amount) FROM book) - amount AS "Заказ"
FROM book
WHERE amount < (SELECT MAX(amount) FROM book);

-- Задание 6: Средняя цена и стоимость для книг 5-14 экз. (аналогично Отчёту 2)
SELECT 
    ROUND(AVG(price), 2) AS "Средняя цена",
    ROUND(SUM(price * amount), 2) AS "Стоимость"
FROM book
WHERE amount BETWEEN 5 AND 14;
