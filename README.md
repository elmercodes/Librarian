# AI Chatbot with Database Access

This project utilizes the OpenAI API to create an AI chatbot capable of engaging in conversations. The chatbot is trained on a knowledge document to learn its responsibilities and is integrated with a PostgreSQL database to fetch information. Additionally, Flask is used to expose the chatbot's functionality as RESTful APIs, allowing integration with pre-built chatbot applications.

## Features

- **OpenAI API Integration**: Utilizes the OpenAI API to create an AI chatbot capable of natural language understanding and generation.
- **Knowledge Document Training**: The chatbot is trained using a knowledge document to learn its responsibilities and tasks.
- **Database Access**: Integrated with a PostgreSQL database to fetch information and responses.
- **RESTful APIs**: Exposes chatbot functionalities as RESTful APIs using Flask, enabling seamless integration with existing chatbot applications.
- **Easy Setup**: Requires minimal setup by users, only needing to update SQL calls, create their database, and link their chatbot applications.
- **Secure Handling of Sensitive Information**: Users are reminded to handle sensitive information securely, such as database credentials, by providing instructions and utilizing environment variables.

## Files and Directories

- **.gitignore**: Excludes certain files and directories from version control, including `.idea`, `__pycache__`, and `venv`.
- **README.md**: This detailed readme file providing an overview of the project, its features, and instructions for setup.
- **SQLconnection.py**: Python script for connecting to the PostgreSQL database and executing SQL queries.
- **functions.py**: Additional Python script containing helper functions for the project.
- **knowledge.docx**: Knowledge document used to train the chatbot on its responsibilities and tasks.
- **main.py**: Main Python script containing the implementation of the AI chatbot with database access.
- **prompts.py**: Python script containing prompts used for training the chatbot.
- **requirements.txt**: File listing the required Python packages and dependencies for the project.

## Getting Started

To get started with the project, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using the following command:
git clone https://github.com/elmercodes/Librarian.git


2. **Set up the Database**: Create a PostgreSQL database and update the SQL calls in `SQLconnection.py` to connect to your database.

3. **Install Dependencies**: Install the required Python packages and dependencies listed in `requirements.txt` using pip:
pip install -r requirements.txt


4. **Update Environment Variables**: Update the sensitive information such as database credentials in your operating system environment variables or in a `.env` file.

5. **Run the Application**: Run the Flask application to start the RESTful APIs:
python main.py


6. **Integrate with Chatbot Application**: Integrate the exposed RESTful APIs with your existing chatbot applications by making HTTP requests to the provided endpoints.

## Contribution

Contributions to the project are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, feel free to submit a pull request.
