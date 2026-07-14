from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [('auth', '0012_alter_user_first_name_max_length')]
    operations = [
        migrations.CreateModel(name='DrugReview', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('drug_name', models.CharField(db_index=True, max_length=200)),
            ('condition', models.CharField(db_index=True, max_length=200)),
            ('review', models.TextField()),
            ('rating', models.FloatField()),
            ('useful_count', models.IntegerField(default=0)),
            ('sentiment', models.CharField(choices=[('positive','Positive'),('neutral','Neutral'),('negative','Negative')], default='neutral', max_length=20)),
            ('sentiment_score', models.FloatField(default=0.0)),
            ('pos_score', models.FloatField(default=0.0)),
            ('neg_score', models.FloatField(default=0.0)),
            ('neu_score', models.FloatField(default=0.0)),
            ('compound_score', models.FloatField(default=0.0)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ], options={'ordering': ['-created_at'], 'verbose_name': 'Drug Review'}),
        migrations.CreateModel(name='Prediction', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('symptoms', models.TextField()),
            ('predicted_condition', models.CharField(db_index=True, max_length=200)),
            ('nb_prediction', models.CharField(blank=True, max_length=200)),
            ('rf_prediction', models.CharField(blank=True, max_length=200)),
            ('svm_prediction', models.CharField(blank=True, max_length=200)),
            ('lr_prediction', models.CharField(blank=True, max_length=200)),
            ('nb_confidence', models.FloatField(default=0)),
            ('rf_confidence', models.FloatField(default=0)),
            ('svm_confidence', models.FloatField(default=0)),
            ('lr_confidence', models.FloatField(default=0)),
            ('model_used', models.CharField(default='ensemble', max_length=100)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ], options={'ordering': ['-created_at']}),
        migrations.CreateModel(name='DrugComparison', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('condition', models.CharField(max_length=200)),
            ('drug_a', models.CharField(max_length=200)),
            ('drug_b', models.CharField(max_length=200)),
            ('winner', models.CharField(blank=True, max_length=200)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name='UserProfile', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('role', models.CharField(choices=[('user','Patient User'),('admin','Administrator')], default='user', max_length=10)),
            ('phone', models.CharField(blank=True, max_length=20)),
            ('age', models.IntegerField(blank=True, null=True)),
            ('gender', models.CharField(blank=True, max_length=10)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
        ]),
        migrations.CreateModel(name='SavedDiagnosis', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('symptoms', models.TextField()),
            ('condition', models.CharField(db_index=True, max_length=200)),
            ('top_drug', models.CharField(blank=True, max_length=200)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diagnoses', to='auth.user')),
        ], options={'ordering': ['-created_at']}),
        migrations.CreateModel(name='DrugInteractionCheck', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('drugs_checked', models.TextField()),
            ('interactions_found', models.IntegerField(default=0)),
            ('severity', models.CharField(blank=True, max_length=20)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ], options={'ordering': ['-created_at']}),
        migrations.CreateModel(name='SearchLog', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True)),
            ('query', models.CharField(max_length=300)),
            ('search_type', models.CharField(default='drug', max_length=50)),
            ('results', models.IntegerField(default=0)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ], options={'ordering': ['-created_at']}),
    ]
