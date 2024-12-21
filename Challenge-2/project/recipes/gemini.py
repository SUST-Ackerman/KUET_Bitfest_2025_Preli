import os

import google.generativeai as genai

from project.settings import env
from project.singleton import Singleton
from recipes.models import Ingredient


class Gemini(metaclass=Singleton):

    def __init__(self):
        self.file_path = 'my_fav_recipes.txt'
        if not os.path.exists(self.file_path):
            open(self.file_path, 'w').close()

        self.GOOGLE_API_KEY = env('GEMINI_API_KEY')
        genai.configure(api_key=self.GOOGLE_API_KEY)
        self.geminiModel = genai.GenerativeModel('gemini-pro')

    def generate_response(self, prompt):
        return self.geminiModel.generate_content(prompt).text

    def add_recipe(self, recipe):
        with open(self.file_path, 'a') as file:
            file.write(recipe + '\n')

    def get_recipe(self, recipe_name):
        with open(self.file_path, 'r') as file:
            recipes = file.readlines()
            response = None
            for i in range(0, len(recipes), 100):
                response = self.geminiModel.generate_content([
                    f'Give me the recipe for {recipe_name} from the below list, if the below list does not have the recipe i am looking for, then return only -1, if found then return the recipe in concise and good format',
                    str(recipes[i:i + 100])
                ]).text

                print(str(recipes[i:i + 100]))
                print(response)

                if len(response) > 5:
                    break

            return response if response != '-1' else 'Recipe not found'

    def suggest_recipe(self, prompt):
        ingredients = str(list(Ingredient.objects.all().values('name', 'quantity', 'unit')))

        with open(self.file_path, 'r') as file:
            recipes = file.readlines()
            response = None
            for i in range(0, len(recipes), 100):
                msg = f'''{prompt}
                    

I was suggested this recipe by someone: {response}
Give me better suggestion than this if possible. 
                    
Return a html response of a recipe from below recipes and available ingredients. If the below list does not have the recipe you are looking for, then return only this string - "None". If found, then return the recipe in concise and good format.
                    
Available Ingredients: {ingredients}

Available Recipes: {str(recipes[i:i + 100])}


your response should be in html format, with good css styling in the html format. only return the html, nothing else.
                    '''

                response = self.geminiModel.generate_content([msg]).text
                if '```html' in response:
                    response = response.split('```html')[1].split('```')[0]

            return response if response != 'None' else 'No such recipe found'
