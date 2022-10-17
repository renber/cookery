from enum import Enum
from pony.orm import desc
from pyapp.dao.entities import Recipe

class RecipeSortOrder(Enum):
    '''
    Represents sort order of recipes
    '''
    latest_first = 'latest_first'
    oldest_first = 'oldest_first'
    alphabetical_asc = 'alphabetical_asc'
    alphabetical_desc = 'alphabetical_desc'

    def getOrmOrderTerm(self):
        '''
        Return the term to use in the ORM's order_by method
        '''
        prop = None

        if self in [self.latest_first, self.oldest_first]:
            prop = Recipe.rec_created_on

        if self in [self.alphabetical_asc, self.alphabetical_desc]:
            prop = Recipe.rec_title

        if self in [self.latest_first, self.alphabetical_desc]:
            prop = desc(prop)
        
        return prop