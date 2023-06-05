from locust import HttpUser, task, between
from locust.exception import RescheduleTask
import json, random
from bs4 import BeautifulSoup
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# [6]
class UserTests(HttpUser):
    count = 0
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        UserTests.count += 1
        self.current_user_id = None
        self.current_username = None
        self.current_password = None
        self.recipe_ids = set([])
        self.cookbook_ids = set([])

    # [4]
    @classmethod
    def generate_user_details(cls):
        cls.count += 1
        name = f"user{cls.count}"
        username = f"user{cls.count}"
        email = f"{name}@gmail.com"
        hashed_password = bcrypt.generate_password_hash(name).decode('utf-8')   
        return name,username, email, hashed_password
        
    # [4]
    def register_user(self):
        global count
        with self.client.get('/api/v1/auth/register', catch_response=True) as response:  # Perform a GET request to retrieve the form
            if response.status_code != 200:
                response.failure(f"Add user request resulted in a {response.status_code} status code. Should return 200.")
            html_content = response.text # Extract the CSRF token from the response

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the attributes from the HTML
            csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

            # Prepare the form data with your desired values
            name, username, email, hashed_password = self.generate_user_details()
            form_data = {
                'name': name,
                'username': username,
                'email': email,
                'password': hashed_password,
                'csrf_token': csrf_token 
            }
            self.current_username=username
            self.current_password=name

            # Perform a POST request with the form data
            with self.client.post('/api/v1/auth/register', data=form_data, catch_response=True) as post_response:
                if post_response.status_code != 200:
                    post_response.failure(f"Add user request resulted in a {post_response.status_code} status code. Should return 200.")


    def login(self):
        global count
        with self.client.get('/api/v1/auth/login', catch_response=True) as response:  # Perform a GET request to retrieve the form
            if response.status_code != 200:
                response.failure(f"Add user request resulted in a {response.status_code} status code. Should return 200.")
            html_content = response.text # Extract the CSRF token from the response

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the attributes from the HTML
            csrf_token = soup.find('input', {'name': 'csrf_token'})['value']

            # Prepare the form data with your desired values
            name, username, email, hashed_password = self.generate_user_details()
            form_data = {
                'username': self.current_username,
                'password': self.current_password,
                'csrf_token': csrf_token 
            }
            
            # Perform a POST request with the form data
            with self.client.post('/api/v1/auth/login', data=form_data, catch_response=True) as post_response:
                if post_response.status_code != 200:
                    post_response.failure(f"Add user request resulted in a {post_response.status_code} status code. Should return 200.")
                else:
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')
                    author_id = soup.find('input', {'name': 'author_id'})['value']
                    self.current_user_id = author_id


    def on_start(self):
        self.register_user()
        # TODO: Create several recipes -> save recipe ids to list
        self.login()
        self.create_recipe(recipe_kw="chicken")
        # TODO: Create several cookbooks -> save cookbook ids to list
        self.create_cookbook()

    @task
    def create_recipe(self, recipe_kw=None):
        with self.client.get('/api/v1/recipe/create_recipe', catch_response=True) as response:  # Perform a GET request to retrieve the form
            if response.status_code != 200:
                response.failure(f"Add user request resulted in a {response.status_code} status code. Should return 200.")
            html_content = response.text # Extract the CSRF token from the response

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the attributes from the HTML
            csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
            author_id = soup.find('input', {'name': 'author_id'})['value']

            # Prepare the form data with your desired values

            with open("backend/data/recipes.json") as f:
                recipe_json = json.load(f)
            if recipe_kw:
                for recipe in recipe_json:
                    if recipe_kw.casefold() in recipe["description"].casefold():
                        recipe_data = recipe
                        break
            else:
                recipe_data = random.choice(recipe_json)
            
            # recipe_data["csrf_token"] = csrf_token

            with self.client.post(f"/api/v1/recipe/create/{self.current_user_id}",json=recipe_data, catch_response=True) as response:
                if response.status_code != 201:
                    
                    response.failure(f"Create recipe request resulted in a {response.status_code} status code. Should return 201.")
                # response_json = response.json()


    @task
    def create_cookbook(self):
        # with open("../data/cookbooks.json") as f:
        #     cookbook_json = json.load(f)
        cookbook_int = len(self.cookbook_ids) + 1
        cookbook_data = {"title": f"Cookbook {cookbook_int} for User {self.current_user_id}"}
        with self.client.post(f"/api/v1/cookbook/create/{self.current_user_id}",json=cookbook_data, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Create cookbook request resulted in a {response.status_code} status code. Should return 201.")
            response_json = response.json()
            self.cookbook_ids.add(int(response_json["id"]))

    @task
    def view_user_recipes(self):
        with self.client.get(f"/api/v1/recipe/get_user_recipes/{self.current_user_id}", catch_response=True) as recipe_resp:

            # Code taken from [4]
            # ******* START *******
            # Access the rendered HTML content
            html_content = recipe_resp.text

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the attributes from the HTML
            recipes = soup.find('input', {'name': 'user_recipes'})['value']

            # ******* END *******
            if recipe_resp.status_code != 200:
                recipe_resp.failure(f"View user recipes request resulted in a {recipe_resp.status_code} status code. Should return 200.")
            if len(recipes) < 1:
                recipe_resp.failure(f"No recipes for user {self.current_user_id}!")

    # @task
    # def view_all_users_recipes(self):
    #     pass

    @task
    def view_user_cookbooks(self):
        with self.client.get(f"/api/v1/cookbook/get_user_cookbooks/{self.current_user_id}", catch_response=True) as cookbook_resp:

            # Code taken from [4]
            # ******* START *******
            # Access the rendered HTML content
            html_content = cookbook_resp.text

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extract the attributes from the HTML
            cookbooks = soup.find('input', {'name': 'user_cookbooks'})['value']

            # ******* END *******
            if cookbook_resp.status_code != 200:
                cookbook_resp.failure(f"View user cookbooks request resulted in a {cookbook_resp.status_code} status code. Should return 200.")
            if len(cookbooks) < 1:
                cookbook_resp.failure(f"No cookbooks for user {self.current_user_id}!")


    # @task
    # def view_user_recipes_in_cookbook(self):
    #     pass

    @task
    def add_recipe_to_cookbook(self):
        # Choose random recipe
        random_recipe_id = random.choice(list(self.recipe_ids))

        # Choose random cookbook
        random_cookbook_id = random.choice(list(self.cookbook_ids))

        add_recipe_to_cookbook_data = {"recipe_id": random_recipe_id, 
                                        "cookbook_id": random_cookbook_id}
        # Add recipe to cookbook
        with self.client.post("/api/v1/cookbook/add_recipe",json=add_recipe_to_cookbook_data, catch_response=True) as response:
            if response.status_code != 201:
                response.failure(f"Add recipe to cookbook request resulted in a {response.status_code} status code. Should return 201.")
        
    @task(3)
    def search_recipe_by_desc(self):
        # search by desc 1
        keywords = "chicken"
        with self.client.get(f"/api/v1/search/searchdescription/{keywords}", catch_response=True) as response:
        
            if response.status_code != 200:
                raise RescheduleTask()
            words = keywords.split(" ")
            response_json = response.json()
            for item in response_json:
                for word in words:
                    if word.casefold() in item["description"].casefold():
                        response.success()
                    else:
                        response.failure(f"{word} is not in {response_json['title']}'s recipe description.")


    @task
    def search_recipe_by_category(self):
        # search by category 1
        keywords = "japanese"
        with self.client.get(f"/api/v1/search/searchcategory/{keywords}", catch_response=True) as response:
            if response.status_code != 200:
                raise RescheduleTask()
        
            words = keywords.split(" ")
            response_json = response.json()
            for item in response_json:
                for word in words:
                    if word.casefold() in item["category"].casefold():
                        response.success()
                    else:
                        response.failure(f"{word} is not {response_json['title']}'s recipe category.")

    # @task
    # def update_recipe(self):
    #     random_recipe_id = random.choice(list(self.recipe_ids))
    #     updated_title = random_recipe_id["title"] + " Updated"
    #     updated_desc = random_recipe_id["description"].split(" ")[:-1]
    #     updated_category = random_recipe_id["category"].upper()
    #     updated_visibility = "PRIVATE" if random_recipe_id["visibility"] == "PUBLIC" else "PUBLIC"
    #     updated_data = {"title":  }
    #     with self.client.post(f"/api/v1/recipe/update/{random_recipe_id}",) as update_recipe_resp:
    #         if update_recipe_resp.status_code != 200:
    #             response.failure(f"Update recipe endpoint resulted in a {update_recipe_resp.status_code} status code. Should return 200.")
    #         response_json = update_recipe_resp.json()

            

    
# ******* START *******

# Access the rendered HTML content
# html_content = recipe_resp.text

# Parse the HTML content with BeautifulSoup
# soup = BeautifulSoup(html_content, 'html.parser')

# Extract the attributes from the HTML
# recipes = soup.find('input', {'name': 'user_recipes'})['value']
# title = soup.find('input', {'name': 'title'}).string
# description = soup.find('input', {'name': 'description'}).string
# category = soup.find('input', {'name': 'category'}).string
# visibility = soup.find('input', {'name': 'visibility'}).string
# author_id = soup.find('input', {'name': 'author_id'}).string

# Use the extracted attributes as needed in your Locust test logic
# print(f"Recipe ID: {recipes}")
# print(f"Title: {title}")
# print(f"Description: {description}")
# print(f"Category: {category}")
# print(f"Visibility: {visibility}")
# print(f"Author ID: {author_id}")