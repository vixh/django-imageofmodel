# -*- coding: utf-8 -*-

from imagekit.specs import ImageSpec 
from imagekit import processors 

# first we define our thumbnail resize processor 
class ResizeThumb(processors.Resize): 
    width = 180 
    height = 120 
    crop = True

# first we define our thumbnail resize processor 
class SmallResizeThumb(processors.Resize): 
    width = 90 
    height = 60 
    crop = True

# now we define a display size resize processor
class ResizeDisplay(processors.Resize):
    width = 800
    height = 600

# now lets create an adjustment processor to enhance the image at small sizes 
class EnchanceThumb(processors.Adjustment): 
    contrast = 1.2 
    sharpness = 1.1 

# now we can define our thumbnail spec 
class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = True 
    processors = [ResizeThumb, EnchanceThumb]

# now we can define our thumbnail spec 
class SmallThumbnail(ImageSpec): 
    access_as = 'small_thumbnail_image' 
    pre_cache = True 
    processors = [SmallResizeThumb, EnchanceThumb] 

# and our display spec
class Display(ImageSpec):
    increment_count = True
    pre_cache = True 
    processors = [ResizeDisplay]