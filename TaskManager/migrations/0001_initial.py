# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Projects'
        db.create_table(u'TaskManager_projects', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('IsCompleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('StartDate', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('EndDate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'TaskManager', ['Projects'])

        # Adding model 'TaskStatus'
        db.create_table(u'TaskManager_taskstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='initiated', max_length=150)),
        ))
        db.send_create_signal(u'TaskManager', ['TaskStatus'])

        # Adding model 'Tasks'
        db.create_table(u'TaskManager_tasks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ProjectId', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['TaskManager.Projects'])),
            ('TaskTitle', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('Description', self.gf('django.db.models.fields.TextField')()),
            ('Requirement', self.gf('django.db.models.fields.TextField')()),
            ('Owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Owner', to=orm['auth.User'])),
            ('Designer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Designer', to=orm['auth.User'])),
            ('Developer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Developer', to=orm['auth.User'])),
            ('Status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['TaskManager.TaskStatus'])),
            ('StartDate', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('EndDate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'TaskManager', ['Tasks'])

        # Adding model 'TaskTrack'
        db.create_table(u'TaskManager_tasktrack', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['TaskManager.Projects'])),
            ('taskid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['TaskManager.Tasks'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['TaskManager.TaskStatus'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'TaskManager', ['TaskTrack'])


    def backwards(self, orm):
        # Deleting model 'Projects'
        db.delete_table(u'TaskManager_projects')

        # Deleting model 'TaskStatus'
        db.delete_table(u'TaskManager_taskstatus')

        # Deleting model 'Tasks'
        db.delete_table(u'TaskManager_tasks')

        # Deleting model 'TaskTrack'
        db.delete_table(u'TaskManager_tasktrack')


    models = {
        u'TaskManager.projects': {
            'EndDate': ('django.db.models.fields.DateField', [], {}),
            'IsCompleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Meta': {'object_name': 'Projects'},
            'StartDate': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'Title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'TaskManager.tasks': {
            'Description': ('django.db.models.fields.TextField', [], {}),
            'Designer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Designer'", 'to': u"orm['auth.User']"}),
            'Developer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Developer'", 'to': u"orm['auth.User']"}),
            'EndDate': ('django.db.models.fields.DateField', [], {}),
            'Meta': {'object_name': 'Tasks'},
            'Owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Owner'", 'to': u"orm['auth.User']"}),
            'ProjectId': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['TaskManager.Projects']"}),
            'Requirement': ('django.db.models.fields.TextField', [], {}),
            'StartDate': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'Status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['TaskManager.TaskStatus']"}),
            'TaskTitle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'TaskManager.taskstatus': {
            'Meta': {'object_name': 'TaskStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'initiated'", 'max_length': '150'})
        },
        u'TaskManager.tasktrack': {
            'Meta': {'object_name': 'TaskTrack'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['TaskManager.Projects']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['TaskManager.TaskStatus']"}),
            'taskid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['TaskManager.Tasks']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['TaskManager']