# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailRemainder'
        db.create_table('bibliotheca_mailremainder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('borrowing', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bibliotheca.Borrowings'])),
            ('sent_mails', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('bibliotheca', ['MailRemainder'])


    def backwards(self, orm):
        # Deleting model 'MailRemainder'
        db.delete_table('bibliotheca_mailremainder')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bibliotheca.authors': {
            'Meta': {'object_name': 'Authors'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bibliotheca.books': {
            'ISBN': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Meta': {'object_name': 'Books'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bibliotheca.Authors']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Categories']"}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_title': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '255'}),
            'published_date': ('django.db.models.fields.IntegerField', [], {}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Publishers']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bibliotheca.borrowings': {
            'Meta': {'object_name': 'Borrowings'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Books']"}),
            'date_since': ('django.db.models.fields.DateTimeField', [], {}),
            'date_to': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Readers']"})
        },
        'bibliotheca.categories': {
            'Meta': {'object_name': 'Categories'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'top_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Categories']", 'null': 'True', 'blank': 'True'})
        },
        'bibliotheca.mailremainder': {
            'Meta': {'object_name': 'MailRemainder'},
            'borrowing': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Borrowings']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_mails': ('django.db.models.fields.IntegerField', [], {})
        },
        'bibliotheca.news': {
            'Meta': {'object_name': 'News'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'text_body': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bibliotheca.publishers': {
            'Meta': {'object_name': 'Publishers'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'bibliotheca.readers': {
            'Meta': {'object_name': 'Readers'},
            'address_aptno': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_postcode': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_strno': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']"})
        },
        'bibliotheca.reservations': {
            'Meta': {'object_name': 'Reservations'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Books']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reader': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Readers']"}),
            'reservation_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'bibliotheca.warehouse': {
            'Meta': {'object_name': 'Warehouse'},
            'book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bibliotheca.Books']"}),
            'books_available': ('django.db.models.fields.IntegerField', [], {}),
            'books_quantity': ('django.db.models.fields.IntegerField', [], {}),
            'books_reserved': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bibliotheca']