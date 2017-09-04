#-*- coding: utf-8 -*-

import sys
import djclick as click

from auth_extra.models import User
from rest_framework.authtoken.models import Token

@click.group()
def cli():
    pass


@cli.command()
@click.option('--email', '-e', required=True)
@click.option('--password', '-p', required=False, help='If left empty a "non login" password will be set')
@click.option('--token', '-t', required=False, help='If left empty a token will be generated')
def create_service_user(email, password, token):

    click.secho('Create service user: {}'.format(email), fg='green')

    try:
        user = User.objects.get(email=email)
        click.secho('User already exists: {}'.format(user), fg='yellow')
        click.secho('Current auth token:  {}'.format(user.auth_token), fg='white')

        if click.confirm('Do you want to delete this user account?'):
            user.delete()
        else:
            click.secho('Exiting.', fg='yellow')
            sys.exit()


    except User.DoesNotExist:
        pass

    user = User.objects.create_user(email=email, password=password)
    click.secho('Created user: {}'.format(user), fg='green')

    if token:
        Token.objects.filter(user=user).update(key=token)

    auth_token = Token.objects.get(user=user)

    click.secho('Current auth token:  {}'.format(auth_token), fg='green')
