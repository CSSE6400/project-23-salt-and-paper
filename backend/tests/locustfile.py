from locust import HttpUser, task, between
import json, random
from bs4 import BeautifulSoup


class UserTests(HttpUser):
    wait_time = between(1, 5)
    current_user_id = None

    def add_user(self):
        with open("../data/users.json") as f:
            user_json = json.load(f)
        
        user_data = random.choice(user_json)
        response_dict = self.client.post("/api/v1/users/create_user", json=user_data)
        response = response_dict.json()
        current_user_id = response['id']

    def on_start(self):
        self.add_user()
        # TODO: Create several recipes -> save recipe ids to list
        self.create_recipe()
        # TODO: Create several cookbooks -> save cookbook ids to list

    @task
    def create_recipe(self):
        with open("../data/recipes.json") as f:
            recipe_json = json.load(f)
        recipe_data = random.choice(recipe_json)
        response_dict = self.client.post(f"/api/v1/recipe/create/{current_user_id}",json=recipe_data)

        # Access the rendered HTML content
        html_content = response.content.decode('utf-8')

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the attributes from the HTML
        recipe_id = soup.find('input', {'name': 'id'})['value']
        title = soup.find('input', {'name': 'title'})['value']
        description = soup.find('input', {'name': 'description'})['value']
        category = soup.find('input', {'name': 'category'})['value']
        visibility = soup.find('input', {'name': 'visibility'})['value']
        author_id = soup.find('input', {'name': 'author_id'})['value']

        # Use the extracted attributes as needed in your Locust test logic
        print(f"Recipe ID: {recipe_id}")
        print(f"Title: {title}")
        print(f"Description: {description}")
        print(f"Category: {category}")
        print(f"Visibility: {visibility}")
        print(f"Author ID: {author_id}")

        # In the example above, BeautifulSoup is imported and used to pa

        pass

    @task
    def create_cookbook(self):
        pass

    @task
    def view_user_recipes(self):
        pass

    @task
    def view_all_users_recipes(self):
        pass

    @task
    def view_user_cookbooks(self):
        pass

    @task
    def view_user_recipes_in_cookbook(self):
        pass

    @task
    def add_recipe_to_cookbook(self):
        pass
        # Randomly choose option 1 or 2

        ## 1. recipe_id = create_recipe()
        ## 2. recipe_id = get_user_recipe()

        # Randomly choose option 1 or 2

        ## 1. cookbook_id = create_cookbook()
        ## 2. cookbook_id = get_user_cookbooks()

        # Add recipe

    @task
    def search_recipe(self):
        pass
        # search by desc 1
        ## assert output has correct substring and is > 0
        # search by desc 2
        ## assert output has correct substring and is > 0

        # search by category 1
        ## assertions

        # search by category 2
    

    @task
    #TODO: Update recipe
    
