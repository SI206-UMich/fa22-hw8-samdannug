import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    # path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    l = []
    cur.execute('select * from restaurants')

    for row in cur.fetchall():
        # print(row)
        d = {}

        name = row[1]

        category_id = row[2]
        cur.execute('select categories.category from categories join restaurants on categories.id = restaurants.category_id where categories.id = ?', (category_id,))
        category = cur.fetchone()[0]

        building_id = row[3]
        cur.execute('select buildings.building from buildings join restaurants on buildings.id = restaurants.building_id where buildings.id = ?', (building_id,))
        building = cur.fetchone()[0]

        rating = row[4]

        d['name'] = name
        d['category'] = category
        d['building'] = building
        d['rating'] = rating

        l.append(d)

    conn.close()
    # print(l)
    return l

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    d = {}
    cur.execute('select * from categories order by category')
    categories = cur.fetchall()
    # print(categories)

    for category in categories:
        curr_id = category[0]
        curr_category = category[1]

        cur.execute('select count(category_id) from restaurants where category_id = ?', (curr_id,))
        curr_count = cur.fetchone()[0]

        d[curr_category] = curr_count


    sorted_d = dict(sorted(d.items(), key=lambda x:x[1]))
    # print(sorted_d.keys())

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.barh(list(sorted_d.keys()), list(sorted_d.values()))

    ax.set_xlabel('Number of Restaurants')
    ax.set_ylabel('Restaurants Categories')
    ax.set_title('Types of Restaurants on South University Ave')
    plt.tight_layout()

    fig.savefig('test.png')
    plt.show()

    # print(d)
    return d

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    get_restaurant_data('South_U_Restaurants.db')
    barchart_restaurant_categories('South_U_Restaurants.db')

class TestHW8(unittest.TestCase):

    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)
    
    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)
    '''
    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)
    '''
if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
