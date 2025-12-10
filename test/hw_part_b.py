from hw_part_a import (
    normalize_addresses,
    add_short_body,
    clean_body_text,
    build_sent_text,
    check_empty_fields,
    mask_sender_email,
    get_correct_email,
    create_email,
    add_send_date,
    extract_login_domain
)


def sender_email(
    recipient_list: list[str],
    subject: str,
    message: str,
    *,
    sender="default@study.com"
) -> list[dict]:

    result = []

    # 1. Проверка пустоты списка получателей
    if not recipient_list:
        return []

    # 2. Проверка корректности email отправителя и получателей
    valid_sender_list = get_correct_email([sender])
    if not valid_sender_list:
        return []

    sender = valid_sender_list[0]

    valid_recipients = get_correct_email(recipient_list)
    if not valid_recipients:
        return []

    # 3. Проверка пустоты темы или текста
    is_sub_empty, is_msg_empty = check_empty_fields(subject, message)
    if is_sub_empty or is_msg_empty:
        return []

    # 4. Исключить отправку себе
    valid_recipients = [
        r for r in valid_recipients if r.lower() != sender.lower()
    ]
    if not valid_recipients:
        return []

    # 5. Нормализация данных
    subject = clean_body_text(subject)
    message = clean_body_text(message)

    sender = normalize_addresses(sender)
    valid_recipients = [normalize_addresses(r) for r in valid_recipients]

    # 6–10 обработка каждого письма
    for r in valid_recipients:

        # 6. Создать письмо
        email = create_email(sender, r, subject, message)

        # 7. Добавить дату
        email = add_send_date(email)

        # 8. Маска отправителя
        login, domain = extract_login_domain(sender)
        email["masked_sender"] = mask_sender_email(login, domain)

        # 9. Короткое тело
        email = add_short_body(email)

        # 10. Итоговый текст
        email["sent_text"] = build_sent_text(email)

        result.append(email)

    return result