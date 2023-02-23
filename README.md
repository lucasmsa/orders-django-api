# 💻 Refera Technical Evaluation API

This project is a web application built with Django that provides a simple interface for managing orders and categories, with an authenticated user. The application is containerized using Docker


### 📝 Set up
---
- To get started with the project, you will need to have Docker installed on your machine. Once you have Docker installed, you can use the following command to build and run the application, Docker was used to make the process of managing dependencies easier, making the project agnostic to the machine it's running on

```
% git clone https://github.com/lucasmsa/refera-technical-evaluation-api.git

% cd refera-technical-evaluation-api

% docker-compose build

% docker-compose up
```

- This will start the application in a Docker container and expose it on port 8000. You can then access the application by opening a web browser and navigating to http://localhost:8000/

### 🖥️ Features
---
- **Tests**: The application was created with TDD approach in mind, in which every business rule related to the entities created was tested. Tests were created using `django_rest_framework` test suite. To execute them run `docker-compose run --rm app sh -c "python manage.py test"`

- **Docs**: All of the application's routes are visible via the `api/docs` url, routes can be tested on the browser using Swagger

- **CI/CD**: A Continuous Integration and Continuous Delivery pipeline was created using Github Actions, which will conduct tests and linting with `flake8`

### ⚙️ Services
---
- **User authentication**: Users can sign up, log in, and see their profiles. Authentication is required to access the orders entity, where the listing of orders is individualized by the user. The authentication was created using AuthToken, adding a `Token <token>` on the `Authorization` header

- **Orders entity**: Users can create, read, update, and delete orders. Orders are associated with a user and a category

- **Public category entity**: It is possible to create, read, update, and delete categories. Categories can be associated with orders and are visible to all users

### ☁️ How could a production environment be created?
---
- **Push the Docker image to a registry**: Once your application is containerized, you'll need to push the Docker image to a registry such as Docker Hub or Amazon ECR. This will make it accessible to your cloud environment

- **Set up the infrastructure**: Create the infrastructure you need to run the application on AWS. This can include resources such as an EC2 instance, a load balancer, a database. You can create these resources manually or use a tool such as AWS CloudFormation or AWS Elastic Beanstalk to create and manage them

- **Configure the environment**: With the infrastructure, you'll need to configure the environment for your application. This can include things like setting environment variables, configuring security groups and network access, and setting up SSL certificates

- **Deploy**: Then it will be possible to deploy the application to the production environment. This can be done using a myriad of tools, such as Kubernetes, Docker Swarm, or AWS ECS. You'll need to specify the Docker image to use, as well as any other configuration options for the container.

### 👾 How should the API be restructured to account for new entities separated from the `Order`?
---
`pk` -> Primary Key
<br>
`fk` -> Foreign Key

- This would individualize the entities and make the orders more based on foreign keys
- In the case of `RealStateAgency`, a new entity could composed of:
```
- id (pk)
- name
- address
- city
- zip_code
```
- As for `Company`, we would have the following fields:
```
- id (pk)
- name
- address
- city
- zip_code
```
- Whereas the `Contact` would be:
```
- id (pk)
- name
- phone
```
- After extracting these entities from the `Order`, it would need to be reestructured too:
```
- id (pk)
- category_id (fk to Category model)
- contact_id (fk to Contact model)
- real_estate_agency_id (fk to RealEstateAgency model)
- company_id (fk to Company model)
- deadline
- description
```
- With this new setup `Order` is now associated with `Company`, `RealStateAgency`, `Contact`. Furthermore, those entities could be joined to have additional informations depending on the purpouse of the operation. 
- The relationship with these entities would be similar than the already established `Category`, consisting in a many-to-one relationship because each `Order` can have exactly one associated `Contact`, `RealEstateAgency`, and `Company`, but each `Contact`, `RealEstateAgency`, and `Company` can be associated with multiple `Order` entities.
