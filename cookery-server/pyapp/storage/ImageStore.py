import os
import shutil
from pyapp import config

class ImageStore:

    def recipe_has_image(self, recipe_id):
        return os.path.isfile (config.IMAGE_STORE_FOLDER + f'/{recipe_id}.jpg')

    def update(self, recipe_id, image_data):
        '''
        Replace the current main image of the recipe with the given id with image data
        '''            
        
        with open(config.IMAGE_STORE_FOLDER + f'/{recipe_id}.jpg', 'wb') as f:
            # write image data to file
            shutil.copyfileobj(image_data, f)        

imageStore = ImageStore()