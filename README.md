# Школьная система тестирования

Данный проект представляет собой программу, созданную для облегчения проведения тестирований различных видов в школах,
но может быть использована и для выполнения других задач. Данная программа предусматривает два типа пользователей
и соответственно два интерфейса: учителя и ученика. Также существует множество дополнительных форм, таких как форма фхода, 
добавление и удаление пользователя и т.д. О них подробнее далее.

## Форма входа

Для работы формы входа нужна база данных содержащая четыре столбца: id, login, password, teacher. Пароль в базе данных
хранится в хэшированном в виде т.е. даже учитель не сможет через базу данных увидеть пароль определенного пользователя.
Для хэширования паролей используется алгоритм SHA-256. Стандартный пароль и логин аккаунта учителя - admin. Стандартный пароль и логин аккаунта ученика - 1.

![Форма входа](https://iili.io/HqqB1I.png)

## Интерфейс учителя

В интерфейсе учителя реализованы две основные функции: создание тестов и редактирование списка учеников.

![Интерфейс учителя](https://iili.io/Hqq1ku.png)

### Создание тестов

Вопросы в тестах могут быть двух типов - один верный ответ, или выбор. Выбрирая первый тип вопроса,
подразумевается паоказ пользователю текст вопроса и поле для ввода ответа. На фото ниже можно увидеть
как выглядит вариант создания вопроса с ответом, вводимым пользователем. Если не будет введен ответ,
или сам текст вопроса, пользователю будет выведено соответствующее сообщение об ошибке. 

![Форма создания теста](https://iili.io/HqqWLQ.png)

Если тип вашего вопроса - Выбор, пользователю будут продемонстрированные введенные вами варианты, рядом с
которым будет поле для отметки. Максимальное количество ответов - 5.

![Тип воароса: выбор](https://iili.io/HqqMIj.png)

При нажатии 'Сохранить вопрос', вопрос соответственно будет сохранен в массив, и отображен в списке
вопросов. Любой вопрос может быть отредактирован, соответственным нажатием на него в списке вопросов,
и изменением каких либо его полей. 
Соответственно при нажатии 'Удалить вопррос', вопрос будет удален.

При нажатии сохранить тест, будет открыто стандартное диалоговое окно, в котором вы сможете выбрать
путь сохранения файла и его имя. При какой лиюо ошибке, связанной с сохранением, будет выведено
соответствующее сообщение.

### Список пользователей

Данная функция реализована для удобного контроля базы данных пользователей со стороны аккаунта преподавателя.

![Список пользователей](https://iili.io/HqqhBV.png)

Реализованы две кнопки отвечающие соответственно отвечающие за добавление и удаления пользователя из базы данных.
Редактировать уже существующего пользователя можно двойным кликом по соответствующей ячейки в таблице.
Изменения в таблице сохраняются нажатием на кнопку Сохранить. Добавление и удаление пользователя сохранения не
требуют. Также, при вводе нового значения в поля 1 и 2 т.е. id и логин, значение проверяется на уникальность.
При вводе нового значения в поле 3 т.е password, программа автоматически хэширует значение.

Значение 4 столбца т.е. teacher задается 1 если пользователь имеет права учителя и 0 если нет
соответственно.

## Интерфейс ученика

Интерфейс ученика заточен под главную цель - прохождение тестов. 

![Интерфейс ученика](https://iili.io/HqqwrP.png)

### Прохождение тестов

Для выполнения этой задачи создан класс в который передается массив с вопросами, и он в автоматическом режиме
настраивает форму на экране под текущий вопрос, считывает ответ пользователя, и в случае окончания списка
вопросов вызывает специализированный класс отвечающий за анализ верных ответов и ответов пользователя, вывод
соответствующего сообщения с результатами.

![Вопрос теста](https://iili.io/HqqeYF.png)

Пример результата теста:

