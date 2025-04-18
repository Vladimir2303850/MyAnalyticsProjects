-- Задание 1: Вывести информацию о всех книгах
SELECT * FROM book;

-- Задание 2: Выбрать авторов, названия и цены книг
SELECT author, title, price FROM book;

-- Задание 3: Выбрать названия и авторов с псевдонимами
SELECT 
    title AS "Название",
    author AS "Автор"
FROM book;

-- Задание 4: Рассчитать стоимость упаковки (1.65 руб за книгу)
SELECT 
    title,
    amount,
    amount * 1.65 AS pack
FROM book;

-- Задание 5: Пересчитать цену со скидкой 30%
SELECT 
    title,
    author,
    amount,
    ROUND(price * 0.7, 2) AS new_price
FROM book;

-- Задание 6: Повысить цены для Булгакова (+10%) и Есенина (+5%)
SELECT 
    author,
    title,
    ROUND(
        CASE 
            WHEN author = 'Булгаков М.А.' THEN price * 1.10
            WHEN author = 'Есенин С.А.' THEN price * 1.05
            ELSE price
        END, 2
    ) AS new_price
FROM book;

-- Задание 7: Книги с количеством меньше 10
SELECT 
    author,
    title,
    price
FROM book
WHERE amount < 10;

-- Задание 8: Книги с ценой <500 или >600 и общей стоимостью >=5000
SELECT 
    title,
    author,
    price,
    amount
FROM book
WHERE (price < 500 OR price > 600) 
  AND (price * amount >= 5000);

-- Задание 9: Книги с ценой 540.50-800 и количеством 2,3,5,7
SELECT 
    title,
    author
FROM book
WHERE price BETWEEN 540.50 AND 800
  AND amount IN (2, 3, 5, 7);

-- Задание 10: Книги с количеством 2-14 (сортировка)
SELECT 
    author,
    title
FROM book
WHERE amount BETWEEN 2 AND 14
ORDER BY author DESC, title ASC;

-- Задание 11: Книги с названием из 2+ слов и инициалами с "С"
SELECT 
    title,
    author
FROM book
WHERE 
    title LIKE '% %' AND
    author LIKE '% С.%'
ORDER BY title ASC;
