# -*- coding: utf-8 -*-from django.db import models
import re, os

from django.db import models
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from imagekit.models import ImageModel
from pytils.translit import slugify as slugify_ru

from fields import ImageTranslifyField


class ModelImagesManager(models.Manager):
    def main_image(self):
        '''
        return main image
        '''
        if self.count():
            return self.all().order_by('order')[0]
        return None
    
    def secondary_images(self):
        '''
        return ordered images without main
        '''
        img_count = self.count()
        if img_count:
            return self.all().order_by('order')[1:img_count]
        return []

class ImageOfModel(ImageModel):
    name = models.CharField(u'Название', max_length=255)
    original_image = ImageTranslifyField(u'Фотка', upload_to='photos')
    num_views = models.PositiveIntegerField(editable=False, default=0)
    order = models.PositiveIntegerField(u'Порядок', blank=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    objects = ModelImagesManager()

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'imageofmodel.specs'
        cache_dir = ''
        cache_filename_format = '%(specname)s/%(filename)s.%(extension)s'
        image_field = 'original_image'
        save_count_as = 'num_views'
    
    class Meta:
        verbose_name = u'Изображение'
        verbose_name_plural = u'Изображения'
        ordering = ('order',)
    
    def __unicode__(self):
        return "%s" % (self.name,)
    
    def img_name(self):
        '''
        Сеошное название. Но не обязательно равно названию картинки на диске, джанго может добавить _ вслучае повторения названия
        Без разширения
        '''
        return '%s-%s' % (slugify_ru(self.name), slugify_ru(self.content_object.__unicode__()))
    
    def save(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self.content_object)
        if self.order is None and self.content_object:
            self.order = (ImageOfModel.objects.filter(content_type__pk=content_type.id, object_id=self.content_object.id).aggregate(Max('order')).get('order__max') or 0) + 10
        
        if self.original_image and self.original_image.file:
            if not re.search(self.img_name(), self.original_image.name): # если картинка нефеншуйная
                name = self.img_name()
                upl_name, ext = os.path.splitext(self.original_image.file.name)
                self.original_image.save(name+ext, self.original_image.file, save=False)
            self.original_image.file.close() # в проверке self.image.file открывает фаил и бывает IOError: [Errno 24] Too many open files
        
        super(self.__class__, self).save(*args, **kwargs)
