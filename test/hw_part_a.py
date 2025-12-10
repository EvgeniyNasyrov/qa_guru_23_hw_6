from datetime import date


# 1. Нормализация email адресов
def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, приведённое к нижнему регистру и очищенное от пробелов по краям.
    """
    return value.strip().lower()


# 2. Сокращенная версия тела письма
def add_short_body(email: dict) -> dict:
    """
    Добавляет email["short_body"] = первые 10 символов тела + "..."
    """
    body = email.get("body", "")
    email["short_body"] = body[:10] + "..." if len(body) > 10 else body
    return email


# 3. Очистка текста письма
def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    return body.replace("\n", " ").replace("\t", " ")


# 4. Формирование итогового текста письма
def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {recipient}, от {sender}
    Тема: {subject}, дата {date}
    {short_body}
    """
    return (
        f"Кому: {email['recipient']}, от {email['sender']}\n"
        f"Тема: {email['subject']}, дата {email['date']}\n"
        f"{email['short_body']}"
    )


# 5. Проверка пустоты темы и тела
def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True — если поле пустое.
    """
    return (not subject.strip(), not body.strip())


# 6. Маска email отправителя
def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    return login[:2] + "***@" + domain


# 7. Проверка корректности email
def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    Корректный email:
    - содержит "@"
    - заканчивается на .com, .ru, .net
    """
    valid_domains = (".com", ".ru", ".net")

    correct = []
    for email in email_list:
        email = email.strip()
        if "@" not in email:
            continue
        if not any(email.endswith(d) for d in valid_domains):
            continue
        correct.append(email)

    return correct


# 8. Создание словаря письма
def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает базовую структуру email.
    """
    return {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }


# 9. Добавление даты отправки
def add_send_date(email: dict) -> dict:
    """
    Добавляет email["date"] = текущая дата в формате YYYY-MM-DD.
    """
    email["date"] = date.today().isoformat()
    return email


# 10. Получение логина и домена
def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен email.
    """
    login, domain = address.split("@")
    return login, domain