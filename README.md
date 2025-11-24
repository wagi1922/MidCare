# MidCare (Backend)

## **Requirements & Tools:**
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![Composer](https://img.shields.io/badge/Composer-885630?style=for-the-badge&logo=composer&logoColor=fff)
![Laravel](https://img.shields.io/badge/Laravel-%23FF2D20.svg?style=for-the-badge&logo=laravel&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=fff)

## **Endpoints:**

1. `/api/auth/login` (POST) = Log in an Admin with credentials.
2. `/api/auth/register` (POST) = Register a new user account.
3. `/api/auth/adminreg` (POST) = Register a new admin account.
4. `/api/admin/categories` (GET) = Get all data from categories.
5. `/api/admin/categories` (POST) = Create a new categories.
6. `/api/admin/questions` (GET) = Colect all questions.
7. `/api/admin/questions` (POST) = Creat a new questons.
8. `/api/admin/questions/{question_id}` (PUT) = Edit a data questions.
9. `/api/admin/questions/{question_id}` (DELETE) = Delete a data questions.
10. `/api/admin/users` (GET) = Get all user list data.
11. `/api/admin/users/result` (GET) = Get all user result.
12. `/api/user/test/questions` (GET) = Get test questions.
13. `/api/user/test/submit` (POST) = Submit the test.
14. `/api/user/result` (GET) = Get result data user.
## **Installation Instructions**

1. Clone the repository:

    ```bash
    git clone https://github.com/wagi1922/MidCare.git
    ```

2. Activate the Virtual Environment:

   ```bash
   .venv\Scripts\Activate.ps1
   ```

3. Upgrade pip:

   ```bash
   python -m pip install --upgrade pip
   ```
   
4. Install Packages:
   
   ```bash
   pip install -r requirements.txt
   ```
   
5. Set up environment variables:
   Create a `.env` file :

   ```bash
   # .env
   SECRET_KEY=" "
   API_KEY=" "
    
    # Kredensial MySQL
    MYSQL_USER=
    MYSQL_PASSWORD=
    MYSQL_HOST=
    MYSQL_DB=
   ```

7. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## **Testing the API**

Use Postman or any API testing tool to test the endpoints. Make sure to include the `Authorization` token and `x-api-key` in the headers for secure
endpoints.

**Postman Documentation:** https://documenter.getpostman.com/view/40220961/2sB3dHWtVi
   

