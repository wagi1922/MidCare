# MidCare (Backend)

## **Requirements & Tools:**
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Composer](https://img.shields.io/badge/Composer-885630?style=for-the-badge&logo=composer&logoColor=fff)
![Laravel](https://img.shields.io/badge/Laravel-%23FF2D20.svg?style=for-the-badge&logo=laravel&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=fff)

## **Endpoints:**

1. `/admin/login` (POST) = Log in an Admin with credentials.
2. `/admin/logout` (POST) = Log out the current admin.
3. `/admin/register` (POST) = Register a new admin account.
4. `/activities` (GET) = Getting List of every activities.
5. `/projects` (GET) = Getting List of every Projects.
6. `/activities/{id_activity}` (GET) = Getting Detail of a specific activity by id.
7. `/projects/{id_project}` (GET) = Getting Detail of a specific project by id.
8. `/admin/activities` (POST) = Creating a new activity.
9. `/admin/projects` (POST) = Creating a new project.
10. `/admin/activities/{id_activity}` (POST/PUT) = Updating an existing activity.
11. `/admin/projects/{id_project}` (POST/PUT) = Updating an existing project.
12. `/admin/activities/{id_activity}` (DEL) = Deleting an existing activity.
13. `/admin/projects/{id_project}` (DEL) = Deleting an existing project.

## **Installation Instructions**

1. Clone the repository:

    ```bash
    git clone https://github.com/Bhayazeed/GrootUIR-Rebuild.git
    ```

2. Install dependencies:

   ```bash
   composer install
   ```

3. Set up environment variables:
   Create a `.env` file with the following `.env.example` configuration:

   ```bash
   API_KEY = "Your API KEY"
   DB_CONNECTION=sqlite
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_DATABASE=laravel
   DB_USERNAME=root
   DB_PASSWORD=
   ```

4. Run the application:
   ```bash
   composer artisan serve
   ```

## **Testing the API**

Use Postman or any API testing tool to test the endpoints. Make sure to include the `Authorization` token and `x-api-key` in the headers for secure
endpoints.

**Postman Documentation:** https://documenter.getpostman.com/view/40883579/2sAYQWKZGB
   

