# AmazingShop
### A minimalist website with a product listing.
#### Languages/framework/technologies: Python3, Django, PostgreSQL database
## Prerequisites
- Docker should be installed on your system. You can download it
  from [here](https://www.docker.com/get-started).

## Installation
### 1. Clone this repository to your local machine and navigate to the local directory:
```bash
  git clone https://github.com/enricoGiga/AmazingShop.git
  cd AmazingShop
```

### 2. Build and Run Docker Containers

Use Docker Compose to build and run the application:

```bash
docker-compose up
```

### 3. Migrate Database and Create Superuser

Once the Docker container is up and running, follow these steps:

1. Make migrations:
   ```bash
   docker-compose exec web python manage.py makemigrations  
   ```
2. Apply the migrations:
   ```bash
   docker-compose exec web python manage.py migrate  
   ```
3. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser 
   ```
 
4. From the admin console, create users as needed and assign them to the appropriate groups (Buyer or Supplier).

## Supplier Dashboard
![sup_view.png](user%2Fstatic%2Fuser%2Fsup_view.png)

## Buyer Dashboard
![buyer_view.png](user%2Fstatic%2Fuser%2Fbuyer_view.png)

##
force rebuild of the image if required:
```bash
docker-compose up --build -d
```
to create a new app:
```bash
python manage.py startapp newapp
```