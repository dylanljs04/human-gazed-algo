# human-gazed-algo

This is code for the Human Gazed Inspired Algorithm.

To start using, please initialize a virtual environment, then proceed to download the necessary libraires by using the command
```
pip install -r requirements.txt
```

## Notes

1. I chose to convert lngitude and latitude of the real world networks into x and y coordinates and then calculate the distance between each node based on the (x,y) coordinates instead of using the optical fibre weights. This is becasue the weights given in the dataset are modified to be 1.25*Haversine/ 1.5*Haversine or 1500km depending on the value of Haversine. 

Thus it is difficult to find the right distances between each node when using the human gaze heuristic or A* heuristic (euclidean distance). 


2. HG4 was removed due to lack of documentation


## ENVIRONMENT VARIABLES REQUIRED
```
OPENAI_API_KEY=XXX
LANGCHAIN_API_KEY=XXX
TAVILY_API_KEY=XXX

# Telegram bot
TELEGRAM_API_KEY=XXX
TELEGRAM_BOT_USERNAME=XXX

# Mongo connection
CHATBOT_MONGO_CONNECTION_STRING
CHATBOT_MONGO_DATABASE=XXX
CHATBOT_MONGO_COLLECTION=XXX
MANAGER_STATUS=XXX

# Initialize tnb keys
TNB_MONGO_CONNECTION_STRING=XXX
TNB_API_KEY=XXX
TNB_API_SECRET=XXX

# GCS bucket name
GCS_BUCKET_NAME=XXX

# Accessing Suria DB credentials
DB_NAME_1=XXX
IAM_USER_1=XXX
INSTANCE_CONNECTION_NAME_1=XXX

# Accessing SIP-CDE DB credentials
DB_NAME_2=XXX
IAM_USER_2=XXX
INSTANCE_CONNECTION_NAME_2=XXX

# Initialize OCR
OCR_API_KEY=XXX
OCR_API_SECRET=XXX

# JWT user
USER_SECRET=XXX
```

IMPORTANT NOTE: Ensure the authenticsation JSON files are added into a folder called "authentication'

### DESCRIPTION
This AI Agent chatbot leverages the LangGraph framework to respond to user queries and perform actions such as downloading bills and sending emails, all based on user requests. Currently, a single-agent chatbot handles all user interactions and actions, but a multi-agent chatbot is also in development.
 
The agent performs tasks by invoking "Tools," which are functions that define specific actions. These functions can be triggered by the chatbot or accessed directly via FastAPI. Further instructions on [adding custom tools](#how-to-add-custom-tools) and [adding databases](#adding-multiple-postgresql-databases-on-cloud-sql-with-iam-authentication) can be found below.

### Important Notes

To run the code locally, there are two different ways to run the program, first is with FastAPI, and the second is with a Telegram Bot. It is important to note that only one mode can be run at a single instance.

### Running Locally with FastAPI

1. Ensure you set up a virtual environment first before installing the libraries required by using the command:

    ```
    pip install -r requirements.txt
    ```
2. Ensure that in `initializer.py`:

    ```
    IS_GOOGLE = False
    ```

3.  To run with FastAPI, ensure `main.py`:

    ```
    from components.routes import fastapi_main

    if __name__ == "__main__":
        fastapi_main()
    ```

4.  Then, run the file `main.py` with the command:
    ```
    python main.py
    ```
    Now, go to your browser and type in the url `http://127.0.0.1:8000/docs`, which will lead you to the FastAPI endpoints.


5.  After that, ensure you log into FastAPI with the proper credentials, under the `OAuth2PasswordBearer (OAuth2, password)` section

6. Use the chatbot under the `single_agent_with_respone` endpoint

before using the chatbot, which is under the `single_agent_with_respone` endpoint. 

### Running Locally with Telegram Bot
1. Ensure you set up a virtual environment first before installing the libraries required by using the command:

    ```
    pip install -r requirements.txt
    ```
2. Ensure that in `initializer.py`:

    ```
    IS_GOOGLE = False
    ```

3. To run with Telegram Bot, first ensure that the `TELEGRAM_API_KEY` and `TELEGRAM_BOT_USERNAME` are specified correctly in the `.env` file:

    ```
    TELEGRAM_API_KEY = XXX
    TELEGRAM_BOT_USERNAME = XXX
    ```

4.  Additionally, the thread_id associated with the telegram bot can be found in the file `telegram_bot.py`. Change the thread_id if you would like to start a new conversation with the telegram bot.

    ```
    thread_id = XXX
    ```

    Changing the thread id is also a good way of rectifying any errors that occur while working on the repo.

5. To run the telegram bot, ensure that `main.py` is as shown:

    ```
    from telegram_bot import telegram_bot

    if __name__ == "__main__":
        telegram_bot()
    ```

6. Finally, run the program by running the command:

    ```
    python main.py
    ```

### Creating Users

To create Users, simply run the code `users.create_user`, which will create a json file that contains all the credential.

After that, import the json file into MongoDB under the collection `brain.users`, and authenticate FastAPI with the credentials.

### HOW TO ADD CUSTOM TOOLS
1. Build the custom tool:
    - define functions (e.g., 'print_tacos')
        - this function can only be called via FastAPI (without agent)

    ```
    def print_tacos():
        x = "i love tacos"
        return x
    ```
    
2. Wrap the function with '@tool'
    - create another function that calls 'print_tacos'
        - this can only be called by the agent
    - mandatory to add a docstring to describe the tool's purpose 
    - IMPORTANT NOTE: Maximum number of characters for docstring is 1024


    ```
    @tool
    def print_tacos_tool():
        """
        Prints and returns a statement that I love tacos, no inputs needed.

        Args:
            None

        Returns:
            str: A string stating "I love tacos".
        """
        x = print_tacos()
        return x
    ```

3. Integrating tools into the agent
    - import the tools into the agent file
    - add tools into 'safe' or 'sensitive' categories

    ```
    e.g.
    from tools.example_tools import print_tacos_tool, print_sensitive_watermelon_tool
    
    ...

    single_agent_safe_tools = [
        TavilySearchResults(max_results=1),
        print_tacos_tool
    ]

    single_agent_sensitive_tools = [
        print_sensitive_watermelon_tool
    ]

    ```

### CHOOSING EMPLOYEE STATUS AND TOOLS

This section will cover ways in whihc you can specify the position of an employee (manager, non-manager, etc) and choose what type of tools are accessible for them.

1. Currently, the manager status is set in the `.env` file, which is then passed into the `agents.single_agent` file. Specify the role of the employee here.
```
MANAGER_STATUS=XXX
```
2. Add in a list of safe tools and sensitive tools that are accesible by this employee in the `agents.single_agent` file like below:
```
manager_safe_tools = [
    tnb_tools.agent_get_electricity_info_for_month,
    tnb_tools.agent_get_statement_information,
    tnb_tools.agent_get_all_account_names,
    db_tools.determine_db_to_query_tool,
    db_tools.python_repl_tool,
    ocr_tools.agent_utilise_ocr,
    ocr_tools.agent_validate_file,
    tnb_tools.agent_edit_tnb_meter_application,
    tnb_tools.agent_fill_up_tnb_meter_application
]

manager_sensitive_tools = [
    tnb_tools.agent_retrieve_monthly_bill_pdf,
]
```

3. To add more positions apart from manager and non-manager, repeat steps 1 and 2 with a different position name and modify the `check_manager` function in `agents.single_agent` file such that it would include the position you added:

    ```
    def check_manager(manager_status):
        if manager_status == "manager":
            ...
        
        elif manager_status == "non-manager":
            ...

        elif manager_status == "NEW_POSITION":
            sensitive_tools = {t.name for t in NEW_POSITION_sensitive_tools}
            single_agent_assistant_runnable = assistant_prompt | llm.bind_tools(
                NEW_POSITION_safe_tools + NEW_POSITION_sensitive_tools
            )
            return single_agent_assistant_runnable, NEW_POSITION_safe_tools, NEW_POSITION_sensitive_tools
    ```


### ADDING MULTIPLE POSTGRESQL DATABASES ON CLOUD SQL WITH IAM AUTHENTICATION
1. Add credentials to .env file
    - for each new database, you need to add the relevant credentials and connection details to your .env file
    - make sure you add the following entries:

    ```
    GOOGLE_APPLICATION_CREDENTIALS_1=path/to/first-service-account.json
    DB_NAME_1=your_first_database_name
    IAM_USER_1=your_first_iam_user
    INSTANCE_CONNECTION_NAME_1=your_first_instance_connection_name

    GOOGLE_APPLICATION_CREDENTIALS_2=path/to/second-service-account.json
    DB_NAME_2=your_second_database_name
    IAM_USER_2=your_second_iam_user
    INSTANCE_CONNECTION_NAME_2=your_second_instance_connection_name
    ```

3. Create connection functions
    - define a lazy_load function in the `components.db` file for each new database, such that the database will only be loaded when it is necessary

    ```
    # Create the suria_db engine lazily
    def lazy_load_suria_db_engine():
        try:
            connector = create_connector(init.SURIA_DB_SERVICE_ACCOUNT_FILE)
            pool = sqlalchemy.create_engine(
                "postgresql+pg8000://",
                creator=lambda: getconn(connector, init.INSTANCE_CONNECTION_NAME_1, init.IAM_USER_1, init.DB_NAME_1),  # Use the getconn_1 function to connect lazily
            )
            
            print("Suria database engine created successfully.")
            return pool
        
        except:
            return "Error connecting to Suria DB"
    ```


4. Write a detailed database summary:
    - Prepare a detailed text summary describing the data stored in the new database. This summary will help the LLM understand the database's content. Write this into a variable named after the new database under the file `components.db_info`, Then add it into the tuple defined at the bottom of the file as shown:
    
    ```
    NEW_DATABASE = "This database stores detailed records of customer transactions, including purchase history, payment methods, and associated metadata. It also contains tables for customer demographics and loyalty program participation."

    files_to_upload: List[Tuple[str, str]] = [
    (DATABASE_1_SUMMARY, "DATABASE_1"),
    (NEW_DATABASE_SUMMARY, "NEW_DATABASE"),
    ...,
    (DATABASE_10_SUMMARY, "DATABASE_10")
    ]
    ```

5. Upload the summary to MongoDB and store its embeddings:
    - convert the summary into embeddings using the LLM model and store these embeddings in MongoDB.
    - `files_to_upload` is tuple defined in `components.db_info`


    for example:
    ```
    @app.get("/upload-all-atlas-vectors")
    async def upload_all_vectors():
        all_records = []  # To store all records for batch insertion

        for file_description, db_name in files_to_upload:
            # Split the text into sections (create a new document for each section)
            df = pd.DataFrame([txt for txt in re.split(r"(?=\n##)", file_description)], columns=["page_content"])
            
            # Add a column for the database name
            df['database_name'] = db_name

            # Generate embeddings using your OpenAI client
            res = init.openai_client.embeddings.create(input=df['page_content'], model=init.DEFAULT_EMBEDDINGS_MODEL)
            embeddings = [data.embedding for data in res.data]
            df['embeddings'] = embeddings
            
            # Convert the DataFrame to a list of dictionaries and append to all_records
            df_dict = df.to_dict(orient="records")
            all_records.extend(df_dict)

        # Insert all the data into MongoDB in one go
        collection = init.mongodb.get_collection(COLLECTION_NAME)
        collection.insert_many(all_records)

        return {
            "message": f"{len(all_records)} vectors uploaded successfully",
        }

    ```
    - replace COLLECTION_NAME with the name of your MongoDB collection

6. Update the database selection logic:
    - modify the `database_collection` to include the new database:

    ```
    # Determine the database to query from the matched vectors
    database_connections = {
    "NEW_DATABASE": lambda: SQLDatabase(engine=lazy_load_new_database_engine(), lazy_table_reflection=True),  # Lazy load for suria_db
    "DATABASE_2": lambda: SQLDatabase(engine=lazy_load_database_2_engine(), lazy_table_reflection=True),  # Lazy load for sip_cde_db
    # Add more databases here by lazily loading them using the `lazy_load_sql_server_engine` function
    # "SIPUF_CPA_DB": lambda: SQLDatabase(engine=lazy_load_sql_server_engine("SIPUF_CPA_DB"), lazy_table_reflection=True)
    }
    ```

Note: If you encounter any issues, verify that your environment variables are correctly set and that your IAM roles and permissions are properly configured.

## Deployment

1. In initializer.py, ensure:
    ```
    IS_GOOGLE = True
    ```

2. In console, ensure that you are pointing to the right project:
    ```
    gcloud config set project brain-433706
    ```

3. Using the supplied `cloud-build.yaml`, use Cloud Build to build the image, run the database migrations, and populate the static assets:
    ```
    gcloud builds submit --config cloud-build.yaml
    ```

4. When the build is successful, deploy the Cloud Run service:
    ```
    gcloud run deploy brain-cloudrun --platform managed --region asia-southeast1 --image gcr.io/brain-433706/brain-cloudrun
    ```

#### 'DETERMINE_DB_TO_QUERY' TOOL
The determine_db_to_query tool is designed to intelligently route SQL queries to the appropriate database by leveraging a pre-built contextual understanding of what is stored in each database. This tool is crucial for systems where multiple databases are involved, and there is a need to determine the most relevant database based on user input. 

Here's how it works:
1. Database Descriptions: each database has a detailed text summary converted into embeddings and stored in MongoDB.
2. Query Matching: the function generates embeddings for the user query and finds the closest matching database descriptions.
3. Contextual Analysis: the matched descriptions are analyzed by an LLM to identify the most relevant database.
4. Database Selection: the query is then routed to the correct PostgreSQL database based on the LLM’s decision.

