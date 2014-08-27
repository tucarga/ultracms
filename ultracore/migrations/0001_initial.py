# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FormField'
        db.create_table(u'ultracore_formfield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('field_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('choices', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('default_value', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('page', self.gf('modelcluster.fields.ParentalKey')(related_name='form_fields', to=orm['ultracore.FormPage'])),
        ))
        db.send_create_signal(u'ultracore', ['FormField'])

        # Adding model 'FormPageTag'
        db.create_table(u'ultracore_formpagetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'ultracore_formpagetag_items', to=orm['taggit.Tag'])),
            ('content_object', self.gf('modelcluster.fields.ParentalKey')(related_name='tagged_items', to=orm['ultracore.FormPage'])),
        ))
        db.send_create_signal(u'ultracore', ['FormPageTag'])

        # Adding model 'FormPage'
        db.create_table(u'ultracore_formpage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailcore.Page'], unique=True, primary_key=True)),
            ('to_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('from_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('sub_menu', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
            ('intro', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
            ('thank_you_text', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
        ))
        db.send_create_signal(u'ultracore', ['FormPage'])

        # Adding model 'StandardPage'
        db.create_table(u'ultracore_standardpage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailcore.Page'], unique=True, primary_key=True)),
            ('body', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
        ))
        db.send_create_signal(u'ultracore', ['StandardPage'])

        # Adding model 'SpecialPageTag'
        db.create_table(u'ultracore_specialpagetag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'ultracore_specialpagetag_items', to=orm['taggit.Tag'])),
            ('content_object', self.gf('modelcluster.fields.ParentalKey')(related_name='tagged_items', to=orm['ultracore.SpecialPage'])),
        ))
        db.send_create_signal(u'ultracore', ['SpecialPageTag'])

        # Adding model 'SpecialPage'
        db.create_table(u'ultracore_specialpage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailcore.Page'], unique=True, primary_key=True)),
            ('feed_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['wagtailimages.Image'])),
            ('sub_menu', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
            ('body', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
        ))
        db.send_create_signal(u'ultracore', ['SpecialPage'])

        # Adding model 'DirectoryPage'
        db.create_table(u'ultracore_directorypage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailcore.Page'], unique=True, primary_key=True)),
            ('body', self.gf('wagtail.wagtailcore.fields.RichTextField')(blank=True)),
        ))
        db.send_create_signal(u'ultracore', ['DirectoryPage'])

        # Adding model 'Advert'
        db.create_table(u'ultracore_advert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link_external', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('link_page', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtailcore.Page'])),
            ('link_document', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['wagtaildocs.Document'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('feed_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['wagtailimages.Image'])),
        ))
        db.send_create_signal(u'ultracore', ['Advert'])

        # Adding model 'Contact'
        db.create_table(u'ultracore_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'ultracore', ['Contact'])

        # Adding M2M table for field tags on 'Contact'
        m2m_table_name = db.shorten_name(u'ultracore_contact_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm[u'ultracore.contact'], null=False)),
            ('tag', models.ForeignKey(orm[u'taggit.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contact_id', 'tag_id'])

        # Adding model 'SiteSetting'
        db.create_table(u'ultracore_sitesetting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailcore.Site'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('site_logo', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['wagtailimages.Image'])),
            ('background_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, on_delete=models.SET_NULL, to=orm['wagtailimages.Image'])),
            ('footer', self.gf('wagtail.wagtailcore.fields.RichTextField')()),
            ('disclaimer', self.gf('wagtail.wagtailcore.fields.RichTextField')()),
        ))
        db.send_create_signal(u'ultracore', ['SiteSetting'])


    def backwards(self, orm):
        # Deleting model 'FormField'
        db.delete_table(u'ultracore_formfield')

        # Deleting model 'FormPageTag'
        db.delete_table(u'ultracore_formpagetag')

        # Deleting model 'FormPage'
        db.delete_table(u'ultracore_formpage')

        # Deleting model 'StandardPage'
        db.delete_table(u'ultracore_standardpage')

        # Deleting model 'SpecialPageTag'
        db.delete_table(u'ultracore_specialpagetag')

        # Deleting model 'SpecialPage'
        db.delete_table(u'ultracore_specialpage')

        # Deleting model 'DirectoryPage'
        db.delete_table(u'ultracore_directorypage')

        # Deleting model 'Advert'
        db.delete_table(u'ultracore_advert')

        # Deleting model 'Contact'
        db.delete_table(u'ultracore_contact')

        # Removing M2M table for field tags on 'Contact'
        db.delete_table(db.shorten_name(u'ultracore_contact_tags'))

        # Deleting model 'SiteSetting'
        db.delete_table(u'ultracore_sitesetting')


    models = {
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'ultracore.advert': {
            'Meta': {'object_name': 'Advert'},
            'feed_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['wagtailimages.Image']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'ultracore.contact': {
            'Meta': {'object_name': 'Contact'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['taggit.Tag']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'ultracore.directorypage': {
            'Meta': {'object_name': 'DirectoryPage', '_ormbases': [u'wagtailcore.Page']},
            'body': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'ultracore.formfield': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'FormField'},
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'field_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'form_fields'", 'to': u"orm['ultracore.FormPage']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'ultracore.formpage': {
            'Meta': {'object_name': 'FormPage'},
            'from_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'intro': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'sub_menu': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'thank_you_text': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'}),
            'to_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'ultracore.formpagetag': {
            'Meta': {'object_name': 'FormPageTag'},
            'content_object': ('modelcluster.fields.ParentalKey', [], {'related_name': "'tagged_items'", 'to': u"orm['ultracore.FormPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'ultracore_formpagetag_items'", 'to': u"orm['taggit.Tag']"})
        },
        u'ultracore.sitesetting': {
            'Meta': {'object_name': 'SiteSetting'},
            'background_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['wagtailimages.Image']"}),
            'disclaimer': ('wagtail.wagtailcore.fields.RichTextField', [], {}),
            'footer': ('wagtail.wagtailcore.fields.RichTextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Site']", 'unique': 'True'}),
            'site_logo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['wagtailimages.Image']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'ultracore.specialpage': {
            'Meta': {'object_name': 'SpecialPage', '_ormbases': [u'wagtailcore.Page']},
            'body': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'}),
            'feed_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['wagtailimages.Image']"}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'sub_menu': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'})
        },
        u'ultracore.specialpagetag': {
            'Meta': {'object_name': 'SpecialPageTag'},
            'content_object': ('modelcluster.fields.ParentalKey', [], {'related_name': "'tagged_items'", 'to': u"orm['ultracore.SpecialPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'ultracore_specialpagetag_items'", 'to': u"orm['taggit.Tag']"})
        },
        u'ultracore.standardpage': {
            'Meta': {'object_name': 'StandardPage', '_ormbases': [u'wagtailcore.Page']},
            'body': ('wagtail.wagtailcore.fields.RichTextField', [], {'blank': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'wagtailcore.page': {
            'Meta': {'object_name': 'Page'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': u"orm['contenttypes.ContentType']"}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'expire_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'go_live_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'has_unpublished_changes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_pages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'search_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'show_in_menus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'wagtailcore.site': {
            'Meta': {'unique_together': "(('hostname', 'port'),)", 'object_name': 'Site'},
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default_site': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'port': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'root_page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites_rooted_here'", 'to': u"orm['wagtailcore.Page']"})
        },
        u'wagtaildocs.document': {
            'Meta': {'object_name': 'Document'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded_by_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'wagtailimages.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'focal_point_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'focal_point_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'focal_point_x': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'focal_point_y': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded_by_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['ultracore']