# -*- coding: utf-8 -*-from django.db import models
from django.db import models
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from imagekit.models import ImageModel
from fields import ImageTranslifyField

class ImageOfModel(ImageModel):
    name = models.CharField(u'Название', max_length=255)
    original_image = ImageTranslifyField(u'Фотка', upload_to='photos')
    num_views = models.PositiveIntegerField(editable=False, default=0)
    order = models.PositiveIntegerField(u'Порядок', blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'imageofmodel.specs'
        cache_dir = 'photos'
        image_field = 'original_image'
        save_count_as = 'num_views'
    
    class Meta:
        verbose_name = u'Изображение'
        verbose_name_plural = u'Изображения'
        ordering = ('order',)
    
    def __unicode__(self):
        return "%s" % (self.name,)
    
    def save(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self.content_object)
        if self.order is None and self.content_object:
            self.order = (ImageOfModel.objects.filter(content_type__pk=content_type.id, object_id=self.content_object.id).aggregate(Max('order')).get('order__max') or 0) + 10
        super(self.__class__, self).save(*args, **kwargs)