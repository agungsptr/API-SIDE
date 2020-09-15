from werkzeug.security import generate_password_hash

import models


def user_seeder():
    try:
        models.User.select().where(models.User.username == 'root').get()
    except models.User.DoesNotExist:
        user = models.User.create(
            id=1,
            name='root',
            username='root',
            password=generate_password_hash('1234567890'),
            telp='000',
            alamat='admin@side',
            jabatan='ADMIN',
            role='ADMIN')
        print({'success': True,
               'username': user.username})
    else:
        print({'success': False,
               'message': 'User is registered'})


if __name__ == '__main__':
    user_seeder()
