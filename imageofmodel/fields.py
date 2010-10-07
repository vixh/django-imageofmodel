from django.db import models
import pytils

class ImageTranslifyField(models.ImageField):
    '''
    Hack translitify cyrrilic file names in ImageField
    '''
    def pre_save(self, model_instance, add):        
        "Returns field's value just before saving."
        file = super(models.FileField, self).pre_save(model_instance, add)
        file.name = pytils.translit.translify(file.name)
        if file and not file._committed:
            # Commit the file to storage prior to saving the model
            file.save(file.name, file, save=False)
        return file