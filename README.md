# MyResearch

I am incorporating [**applehealthdata**](https://github.com/tdda/applehealthdata) as part of our research.
Contains no personal data．

## How to Use

0. Export your healthcare information from your iPhone.

1. Please install Docker.

2. Clone the repository to any directory.

3. Move to that directory and run `docker compose up -d --build`.

4. Create `data` and `extraction_data` folders in the `app` folder.

5. Put the `export.xml` file into the `data` folder and execute `docker compose exec python3 bash`.

6. Next, move to the `app` directory and run `python3 applehealthdata.py data/export.xml`.

7. Finally, run `python3 main.py`.

8. The results will be output to `extraction_data` folders.

9. To exit, run `exit` in the terminal and run `docker compose down`.

## About Functions

### This function allows you to visualize your sleep time and step count.

```python
dataVisualization(mode, file_name)
```

- first argument：Specifying the mode. You can change settings from `settings.json`.
- second argument：File name of the image to output.
<hr>

### This is a function that estimates sleep time from the number of steps.

```python
estimateSleepFromStep(mode, [a, b, c, d], file_name)
```

- first argument：Specifying the mode. You can change settings from `settings.json`.
- second argument：Array with time set．Please set as below. If you add "-" to the threshold value, it becomes the default value (2 hours).
  `[bed_time_average, wake_time_average, bed_time_threshold, step_observation_threshold, wake_time_threshold]`
- third argument：If the time between a step and the next observed step is more than **N hours**, skip the values for that day. Please enter a value between 9 and 24 hours.
- Fourth argument：File name of the image to output.

> - Supports those whose bedtime is after 00:00. It will not work if it is before the day has passed.
> - This does not take into account cases where you wake up in the middle of the day (this will be supported in the future).
