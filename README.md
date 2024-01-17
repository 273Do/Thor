# MyResearch
I am incorporating [**applehealthdata**](https://github.com/tdda/applehealthdata) as part of our research.
Contains no personal data．

## How to Use

1. Please install Docker.

2. Clone the repository to any directory.

3. Move to that directory and run ```docker compose up -d --build```.

4. Create `data` and `extraction_data` folders in the `app` folder.

5. Put the `export.xml` file into the `data` folder and execute ```docker compose exec python3 bash```.

6. Next, move to the `app` directory and run ```python3 applehealthdata.py data/export.xml```.

7. Finally, run ```pyrhon3 main.py```.

8. The results will be output to `extraction_data` folders.

10. To exit, run ```exit``` in the terminal and run ```docker compose down```.
