from locust import HttpUser, task, between
import json, random
from bs4 import BeautifulSoup


class UserTests(HttpUser):
    wait_time = between(1, 5)
    current_user_id = None
    recipe_ids = set()
    cookbook_ids = set()

    def add_user(self):
        with open("../data/users.json") as f:
            user_json = json.load(f)
        
        user_data = random.choice(user_json)
        response = self.client.post("/api/v1/users/create_user", json=user_data)
        assert response.status_code == 201, f"Add user request resulted in a {response.status_code} status code. Should be 201."
        response_dict = response.json()
        UserTests.current_user_id = int(response_dict["id"])

    def on_start(self):
        self.add_user()
        # TODO: Create several recipes -> save recipe ids to list
        self.create_recipe(recipe_kw="chicken")
        # TODO: Create several cookbooks -> save cookbook ids to list
        self.create_cookbook()

    @task
    def create_recipe(self, recipe_kw=None):
        with open("../data/recipes.json") as f:
            recipe_json = json.load(f)
        if recipe_kw:
            for recipe in recipe_json:
                if recipe_kw.casefold() in recipe["description"].casefold():
                    recipe_data = recipe
                    break
        else:
            recipe_data = random.choice(recipe_json)

        response = self.client.post(f"/api/v1/recipe/create/{UserTests.current_user_id}",json=recipe_data)
        assert response.status_code == 201, f"Create recipe request resulted in a {response.status_code} status code. Should be 201."
        response_json = response.json()
        UserTests.recipe_ids.add(int(response_json["id"]))


    @task
    def create_cookbook(self):
        # with open("../data/cookbooks.json") as f:
        #     cookbook_json = json.load(f)
        random_int = random.randrange(10000000)
        cookbook_data = {"title": f"Cookbook {random_int}"}
        response = self.client.post(f"/api/v1/cookbook/create/{UserTests.current_user_id}",json=cookbook_data)
        assert response.status_code == 201, f"Create cookbook request resulted in a {response.status_code} status code. Should be 201."
        response_json = response.json()
        UserTests.cookbook_ids.add(int(response_json["id"]))

    @task
    def view_user_recipes(self):
        recipe_resp = self.client.get(f"/api/v1/recipe/get_user_recipes/{UserTests.current_user_id}")

        # Code taken from [4]
        # ******* START *******
        # Access the rendered HTML content
        html_content = recipe_resp.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the attributes from the HTML
        recipes = soup.find('input', {'name': 'user_recipes'})['value']

        # Use the extracted attributes as needed in your Locust test logic
        # print(f"Recipe ID: {recipes}")
        # ******* END *******
        assert recipe_resp.status_code == 200, f"View user recipes request resulted in a {recipe_resp.status_code} status code. Should be 200."
        assert len(recipes) > 0, f"No recipes for user {UserTests.current_user_id}!"


    # @task
    # def view_all_users_recipes(self):
    #     pass

    @task
    def view_user_cookbooks(self):
        cookbook_resp = self.client.get(f"/api/v1/cookbook/get_user_cookbooks/{UserTests.current_user_id}")

        # Code taken from [4]
        # ******* START *******
        # Access the rendered HTML content
        html_content = cookbook_resp.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract the attributes from the HTML
        cookbooks = soup.find('input', {'name': 'user_cookbooks'})['value']

        # Use the extracted attributes as needed in your Locust test logic
        # print(f"Cookbook ID: {cookbooks}")
        # ******* END *******
        assert cookbook_resp.status_code == 200, f"View user cookbooks request resulted in a {cookbook_resp.status_code} status code. Should be 200."
        assert len(cookbooks) > 0, f"No cookbooks for user {UserTests.current_user_id}!"


    # @task
    # def view_user_recipes_in_cookbook(self):
    #     pass

    @task
    def add_recipe_to_cookbook(self):
        # Choose random recipe
        random_recipe_id = random.choice(list(UserTests.recipe_ids))

        # Choose random cookbook
        random_cookbook_id = random.choice(list(UserTests.cookbook_ids))

        add_recipe_to_cookbook_data = {"recipe_id": random_recipe_id, 
                                        "cookbook_id": random_cookbook_id}
        print(f"Recipe id: {random_recipe_id}")
        print(f'Cookbook id: {random_cookbook_id}')
        # Add recipe to cookbook
        response = self.client.post("/api/v1/cookbook/add_recipe",json=add_recipe_to_cookbook_data)
        assert response.status_code == 201, f"Add recipe to cookbook request resulted in a {response.status_code} status code. Should be 201."
        
    @task
    def search_recipe_by_desc(self):
        # search by desc 1
        keywords = "chicken"
        response = self.client.get(f"/api/v1/search/searchdescription/{keywords}")
        
        ## assert output has correct substring and is > 0
        assert response.status_code == 200, f"Search description endpoint request resulted in a {response.status_code} status code. Should be 200."
        words = keywords.split(" ")
        response_json = response.json()
        for word in words:
            assert word.casefold() in response_json["description"].casefold(), f"{word} is not in {response_json['title']}'s recipe description."


    @task
    def search_recipe_by_category(self):
        # search by category 1
        keywords = "japanese"
        response = self.client.get(f"/api/v1/search/searchcategory/{keywords}")
        
        ## assert output has correct substring and is > 0
        assert response.status_code == 200, f"Search category endpoint request resulted in a {response.status_code} status code. Should be 200."
        words = keywords.split(" ")
        response_json = response.json()
        for word in words:
            assert word.casefold() in response_json["category"].casefold(), f"{word} is not {response_json['title']}'s recipe category."

    # @task
    # #TODO: Update recipe
    
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