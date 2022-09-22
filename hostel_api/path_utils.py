def get_photo_path(instance, filename):
    """Функция для получения пути к фото"""
    file_extension = filename.split('.')[-1]
    return f'photos/{instance.student.surname} {instance.student.student_card}.{file_extension}'


def get_contract_path(instance, filename):
    """Функция для получения пути к файлу договора"""
    return f'contracts/{instance.student.surname} {instance.student.student_card}.pdf'


def get_registration_path(instance, filename):
    """Функция для получения пути к файлу временной регистрации"""
    return f'registrations/{instance.student.surname} {instance.student.student_card}.pdf'
