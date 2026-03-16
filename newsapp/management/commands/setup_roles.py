from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from newsapp.models import Article, Newsletter


class Command(BaseCommand):
    help = "Create default roles and assign permissions"

    def handle(self, *args, **kwargs):
        # Create groups
        reader_group, _ = Group.objects.get_or_create(name="Reader")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        journalist_group, _ = Group.objects.get_or_create(name="Journalist")

        # Article permissions
        view_article = Permission.objects.get(codename="view_article")
        add_article = Permission.objects.get(codename="add_article")
        change_article = Permission.objects.get(codename="change_article")
        delete_article = Permission.objects.get(codename="delete_article")

        # Newsletter permissions
        view_newsletter = Permission.objects.get(codename="view_newsletter")
        add_newsletter = Permission.objects.get(codename="add_newsletter")
        change_newsletter = Permission.objects.get(codename="change_newsletter")
        delete_newsletter = Permission.objects.get(codename="delete_newsletter")

        # Reader permissions
        reader_group.permissions.set([
            view_article,
            view_newsletter,
        ])

        # Editor permissions
        editor_group.permissions.set([
            view_article, change_article, delete_article,
            view_newsletter, change_newsletter, delete_newsletter,
        ])

        # Journalist permissions
        journalist_group.permissions.set([
            add_article, view_article, change_article, delete_article,
            add_newsletter, view_newsletter, change_newsletter, delete_newsletter,
        ])

        self.stdout.write(self.style.SUCCESS("Roles and permissions created successfully."))
